import scrapy
from scrapy.crawler import CrawlerProcess
import os
import re
import json
from scrapy_selenium import SeleniumRequest

# command line args
class GenericNewsSpider(scrapy.Spider):
    name="Generic"
    doNotScrape = [] #list of regex paths

    def start_requests(self):
        yield SeleniumRequest(url=self.starturl, wait_time=3, callback=self.parse)

    # should be overridden
    def has_main_content(self, response):
        return False

    # returns list of content strings
    def get_response_main_content_text(self, response):
        return []

    # return single string for headline
    def get_response_main_content_headline(self, response):
        return ""

    # return single datetime object
    def get_response_publication_date(self, response):
        return ""

    # return list of href objects
    def get_response_href_list(self, response):
        return []

    def parse(self, response):
        # first check if this is a page
        if self.has_main_content(response):
            # get title
            headline = self.get_response_main_content_headline(response)
            # select classes of zn-body__paragraph
            all_text = self.get_response_main_content_text(response)
            final_text = ''
            for text in all_text:
                final_text += text

            pub_date = self.get_response_publication_date(response)
        
            filename = headline.replace(" ", "").replace("\'", "").replace(".", "").replace('\r', "").replace("\n", "")
            output_name = "Scraped/" + self.name + "/" + filename + ".json"
            output_json = {}
            output_json["title"] = headline
            output_json["body"] = final_text
            output_json["url"] = response.request.url
            output_json["date"] = pub_date
            with open(output_name, "w+") as output_fh:
                json.dump(output_json, output_fh)

        # follow links in page
        for link in self.get_response_href_list(response):
            link = response.urljoin(link)
            do_not_parse = False
            for do_not_pattern in self.doNotScrape:
                if re.match(do_not_pattern, link):
                    do_not_parse = True
                    break
            if link.startswith(response.url) and not do_not_parse:
                yield SeleniumRequest(url=link, wait_time=3, callback=self.parse)
