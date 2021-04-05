import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest

class CNNSpider(scrapy.Spider):
    name="CNN"
    start_urls = ["https://www.cnn.com"]

    def start_requests(self):
        yield SeleniumRequest(url="https://www.cnn.com", wait_time=3, callback=self.parse)

    def parse(self, response):
        # first check if this is a page
        all_text = response.css('div.zn-body__paragraph::text').getall()
        if len(all_text) > 0:
            # get title
            headline = response.css('h1.pg-headline::text').getall()
            headline = headline[0]
            # select classes of zn-body__paragraph
            final_text = ''
            for text in all_text:
                final_text += text
        
            filename = headline.replace(" ", "").replace("\'", "")
            output_name = "Scraped/CNN/" + filename + ".json"
            output_json = {}
            output_json["title"] = headline
            output_json["body"] = final_text
            with open(output_name, "w+") as output_fh:
                json.dump(output_json, output_fh)

        # follow links in page
        for link in response.xpath("//a/@href").getall():
            link = response.urljoin(link)
            if link.startswith(response.url):
                yield SeleniumRequest(url=link, wait_time=3, callback=self.parse)
