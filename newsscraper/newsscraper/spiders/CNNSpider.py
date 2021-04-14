import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class CNNSpider(GenericNewsSpider):
    def __init__(self, **kwargs):
        self.name = "CNN"
        self.starturl = "https://www.cnn.com"
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        all_text = response.css('div.zn-body__paragraph::text').getall()
        return len(all_text) > 0

    def get_response_main_content_text(self, response):
        return response.css('div.zn-body__paragraph::text').getall()

    def get_response_main_content_headline(self, response):
        return response.css('h1.pg-headline::text').getall()[0]

    def get_response_publication_date(self, response):
        timeBoxes = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        if timeBoxes is None:
            return ""
        return timeBoxes

    def get_response_href_list(self, response):
        return response.xpath("//a/@href").getall()