import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class NPRSpider(GenericNewsSpider):
    def __init__(self, **kwargs):
        self.name = "NPR"
        self.starturl = "https://www.npr.org/"
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        main_content = response.css("div.storytext")
        if main_content is not None and len(main_content) > 0:
            all_text = main_content[0].css("p::text").getall()
            if len(all_text) > 0:
                return True
        return False

    def get_response_main_content_text(self, response):
        main_content = response.css("div.storytext")
        return main_content[0].css("p::text").getall()

    def get_response_main_content_headline(self, response):
        headline_div = response.css('div.storytitle')[0]
        headline = headline_div.css('h1::text').getall()
        return headline[0]

    def get_response_publication_date(self, response):
        timeblock = response.css('div.dateblock')[0]
        return timeblock.xpath('//time/@datetime').extract_first()

    def get_response_href_list(self, response):
        link_subset = response.xpath("//section[@id='main-section']")
        if len(link_subset) > 0:
            return link_subset[0].xpath("//a/@href").getall()
        return []