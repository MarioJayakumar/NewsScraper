import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from .GenericNewsSpider import GenericNewsSpider

class PGPDSpider(GenericNewsSpider):

    def __init__(self, **kwargs):
        self.name = "PGPD"
        self.starturl = "http://pgpolice.blogspot.com/"
        self.doNotScrape = [r"http://www\.pgpolice\.blogspot\.com/2020/.*", r"http://www\.pgpolice\.blogspot\.com/2019/.*", 
        r"http://www\.pgpolice\.blogspot\.com/2018/.*", r"http://www\.pgpolice\.blogspot\.com/2017/.*", 
        r"http://www\.pgpolice\.blogspot\.com/2016/.*", r"http://www\.pgpolice\.blogspot\.com/2015/.*", 
        r"http://www\.pgpolice\.blogspot\.com/2014/.*", r"http://www\.pgpolice\.blogspot\.com/2013/.*", 
        r"http://www\.pgpolice\.blogspot\.com/2012/.*", r"http://www\.pgpolice\.blogspot\.com/2011/.*", 
        r"http://www\.pgpolice\.blogspot\.com/2010/.*"]
        super().__init__(**kwargs)

    # should be overridden
    def has_main_content(self, response):
        main_text_box = response.xpath("//div[@itemprop='blogPost']")
        if main_text_box is not None and len(main_text_box) > 0:
            all_text = main_text_box[0].css('span::text').getall()
            if len(all_text) > 0:
                return True
        return False

    # returns list of content strings
    def get_response_main_content_text(self, response):
        main_text_box = response.xpath("//div[@itemprop='blogPost']")
        all_text = main_text_box[0].css('span::text').getall()
        return all_text

    # return single string for headline
    def get_response_main_content_headline(self, response):
        headlineBox = response.css("div.post")
        headline = headlineBox.css('h3.post-title::text').getall()
        return headline[0]

    # return single datetime object
    def get_response_publication_date(self, response):
        timeblock = response.css('h2.date-header')
        return timeblock.css("span::text").get(default="")

    # return list of href objects
    def get_response_href_list(self, response):
        return response.xpath("//a/@href").getall()
