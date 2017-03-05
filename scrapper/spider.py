import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy import Item, Field
import csv


class ArticleItem(Item):
    """
    Item class to store value from the scrapper
    """
    title = Field()
    link = Field()
    company = Field()
    company_link = Field()


class JsonWriterPipeline(object):
    """
    Writer pipeline class to write output to csv file
    """
    def __init__(self):
        # Initialize labels as needed
        headers_labels = {'title': 'article title', 'link': 'article url', 'company': 'company name', 'company_link': 'company website'}

        # create output file
        openfile = open('output/output.csv', 'w', newline='')
        fieldnames = ['title', 'link', 'company', 'company_link']
        self.file = csv.DictWriter(openfile, fieldnames=fieldnames)
        self.file.writerow(headers_labels)

    def process_item(self, item, spider):
        self.file.writerow(item)
        return item


class TechCrunchSpider(scrapy.Spider):
    """
    Main Spider class - fetches articles from techcrunch website
    """
    name = 'TechcrunchSpider'

    def start_requests(self):
        url = 'https://techcrunch.com'
        yield scrapy.Request(url=url, callback=self.fetch_urls)

    def fetch_urls(self, response):
        # from techcrunch pull all articles and start processing
        for title in response.css('h2.post-title'):
            next_page = title.css('a ::attr(href)').extract_first()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    """
    Function to parse the response
    1. Parses the response from the url and retrieves company, name, link and title
    2. Writes the above data to csv
    """
    def parse(self, response):
        companies = response.css('ul.crunchbase-accordion > li.crunchbase-card')
        page_title = response.css('h1.tweet-title ::text').extract_first()
        # if no companies write na and write to link
        if not companies:
            article = ArticleItem()
            article['title'], article['link'], article['company_link'], article['company'] = page_title, response.url, 'n/a', 'n/a'
            yield article

        # Handle if many companies exist for one article
        for company in companies:
            company_name = company.css('a.cb-card-title-link ::text').extract_first()
            company_name = company_name.strip() if company_name else 'n/a'
            for card in company.css('li.full'):
                # check for website part and pull the link and company name
                if card.css('.key ::text').extract_first() and card.css('.key ::text').extract_first().lower() == "website":  # lower to handle all possible combinations of 'website'
                    company_link = card.css('.value > a ::text').extract_first()
                    company_link = company_link.strip() if company_link else 'n/a'
                    # yield output - write to csv
                    article = ArticleItem()
                    article['title'], article['link'], article['company_link'], article['company'] = page_title, response.url, company_link, company_name
                    yield article


if __name__ == "__main__":
    """ Main function - initialize settings to connect pipleine and logs"""
    settings = Settings()
    settings.set('ITEM_PIPELINES', {
        '__main__.JsonWriterPipeline': 100
    })
    settings.set('USER_AGENT', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
    settings.set('LOG_LEVEL', 'INFO')
    # Initialize the crawler process
    process = CrawlerProcess(settings)
    process.crawl(TechCrunchSpider)
    process.start()
