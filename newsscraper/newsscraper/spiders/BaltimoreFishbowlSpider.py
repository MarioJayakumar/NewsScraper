import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class BaltimoreFishbowlSpider(GenericNewsSpider):
    def __init__(self, **kwargs):
        self.name = "BaltimoreFishbowl"
        self.starturl = "https://baltimorefishbowl.com/"
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        text_container = response.css("article.post")
        if text_container is not None and len(text_container) > 0:
            all_text = text_container[0].css('p::text').getall()
            if len(all_text) > 0:
                return True        
        return False

    # returns list of content strings
    def get_response_main_content_text(self, response):
        text_container = response.css("article.post")
        all_text = text_container[0].css('p::text').getall()        
        return all_text

    # return single string for headline
    def get_response_main_content_headline(self, response):
        headline = response.css('h1.entry-title::text').getall()
        return headline[0]

    # return single datetime object
    def get_response_publication_date(self, response):
        timeblock = response.css('span.td-post-date')[0]
        return timeblock.xpath('//time/@datetime').extract_first()

    # return list of href objects
    def get_response_href_list(self, response):
        return response.xpath("//a/@href").getall()
