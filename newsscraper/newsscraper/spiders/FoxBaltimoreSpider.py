import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class FoxBaltimoreSpider(GenericNewsSpider):

    def __init__(self, **kwargs):
        self.name = "FoxBaltimore"
        self.starturl = "https://www.foxbaltimore.com/"
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        main_text_box = response.css("div.StoryText-module_storyText__t-_v")
        if main_text_box is not None and len(main_text_box) > 0:
            all_text = main_text_box[0].css("p").getall()
            if len(all_text) > 0:
                return True
        return False

    # returns list of content strings
    def get_response_main_content_text(self, response):
        main_text_box = response.css("div.StoryText-module_storyText__t-_v")
        all_text = main_text_box[0].css("p::text").getall()
        return all_text


    # return single string for headline
    def get_response_main_content_headline(self, response):
        main_text_box = response.css("div.index-module_storyTitle__1sn_")
        headline = main_text_box.css('h1::text').getall()
        return headline[0]

    # return single datetime object
    def get_response_publication_date(self, response):
        timeblock = response.css('div.index-module_bylineTextContainer__1cjf')[0]
        return timeblock.xpath('//time/@datetime').extract_first()

    # return list of href objects
    def get_response_href_list(self, response):
        return response.xpath("//a/@href").getall()
