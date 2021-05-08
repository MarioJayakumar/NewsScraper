import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class WJZSpider(GenericNewsSpider):

    def __init__(self, **kwargs):
        self.name = "WJZ"
        self.starturl = "https://baltimore.cbslocal.com/"
        
        self.doNotScrape = [r"https://baltimore\.cbslocal\.com/video/.*", r"https://baltimore\.cbslocal\.com/photo-galleries/.*", r"https://baltimore\.cbslocal\.com/category/.*"]
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        main_text_box = response.css("div.main-story-wrapper")
        if main_text_box is not None and len(main_text_box) > 0:
            all_text = main_text_box[0].css('p::text').getall()
            if len(all_text) > 0:
                return True
        return False

    # returns list of content strings
    def get_response_main_content_text(self, response):
        main_text_box = response.css("div.main-story-wrapper")
        all_text = main_text_box[0].css('p::text').getall()
        return all_text

    # return single string for headline
    def get_response_main_content_headline(self, response):
        main_text_box = response.css("div.banner-title-wrapper")
        headline = main_text_box.css('h1::text').getall()
        return headline[0]

    # return single datetime object
    def get_response_publication_date(self, response):
        timeblock = response.css("div.column-header")
        return timeblock.css("time.post-date::text").extract_first()

    # return list of href objects
    def get_response_href_list(self, response):
        return response.xpath("//a/@href").getall()
