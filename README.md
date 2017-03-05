# Techcrunch Spider
Note: Built on Scrapy web crawler framework

Scrapy spider which fetches articles from techcrunch.com. Once the article is fetched it'll try to find the company associated with article and writes output to a csv file


## Instalation and Run
1. Create a virtual environment with Python 3 and do following or make sure you have all the libraries as mentioned in requirements.txt.
    
    `> pip install -r requirements.txt`
2. To run the spider
  
    `> python scrapper/spider.py`
3. Output will be written in the folder output as `output.csv`
4. Run tests - from root of the projects enter
    
    `> nosetests`

## Note on Output
If an article is found to associated with many companies, For example: article1 - [company1, company2, company3]
The csv output will contain
  ```
  article1, article1 link, company1, comapny1 link
  article1, article1 link, company2, comapny2 link
  article1, article1 link, company3, comapny3 link
  ```
