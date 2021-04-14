import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class ABCSpider(GenericNewsSpider):
    def __init__(self, **kwargs):
        self.name = "ABC"
        self.starturl = "https://abcnews.go.com/"
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        all_text = response.css('p::text').getall()
        headline = response.css('h1.Article__Headline__Title::text').getall()
        return len(all_text) > 0 and len(headline) > 0

    # returns list of content strings
    def get_response_main_content_text(self, response):
        return response.css('p::text').getall()

    # return single string for headline
    def get_response_main_content_headline(self, response):
        return response.css('h1.Article__Headline__Title::text').getall()[0]

    # return single datetime object
    def get_response_publication_date(self, response):
        timeBoxes = response.css('div.Byline__Meta--publishDate::text').get(default="")
        return timeBoxes

    # return list of href objects
    def get_response_href_list(self, response):
        return response.xpath("//a/@href").getall()

