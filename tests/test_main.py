from scrapper import TechCrunchSpider
from unittest.case import TestCase
from .responses import fake_response_from_file


class SpiderTestCase(TestCase):
    """ Testcases to test the techcrunch spider """
    def setUp(self):
        self.spider = TechCrunchSpider()

    # This function tests a sample which has link title company and company name
    def testParseWithCompany(self):
        result = self.spider.parse(fake_response_from_file('samples/techcrunch1.html', url="https://techcrunch.com/2017/03/04/researcher-finds-bug-that-allows-free-uber-rides/"))
        for item in result:
            self.assertIsNotNone(item['title'])
            self.assertIsNotNone(item['link'])
            self.assertIsNotNone(item['company_link'])
            self.assertIsNotNone(item['company'])

            self.assertEqual(item['title'], "Researcher finds bug that allowed free Uber rides")
            self.assertEqual(item['link'], "https://techcrunch.com/2017/03/04/researcher-finds-bug-that-allows-free-uber-rides/")
            self.assertEqual(item['company'], "Uber")
            self.assertEqual(item['company_link'], "http://www.uber.com")

    # This function tests a sample which has link title but no company and company name
    def testParseWithoutCompany(self):
        result = self.spider.parse(fake_response_from_file('samples/techcrunch2.html', url="https://techcrunch.com/2017/03/04/meet-the-tiny-phone-company-thats-making-modularity-sustainable/"))
        for item in result:
            self.assertIsNotNone(item['title'])
            self.assertIsNotNone(item['link'])
            self.assertIsNotNone(item['company_link'])
            self.assertIsNotNone(item['company'])

            self.assertEqual(item['title'], "Meet the tiny phone company that’s making modularity sustainable")
            self.assertEqual(item['link'], "https://techcrunch.com/2017/03/04/meet-the-tiny-phone-company-thats-making-modularity-sustainable/")
            self.assertEqual(item['company'], "n/a")
            self.assertEqual(item['company_link'], "n/a")
