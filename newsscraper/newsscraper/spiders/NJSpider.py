import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest

class NJSpider(scrapy.Spider):
    name="NJ"
    start_urls = ["https://www.nj.com/"]

    def start_requests(self):
        yield SeleniumRequest(url=self.start_urls[0], wait_time=3, callback=self.parse)

    def parse(self, response):
        # first check if this is a page
        main_text_box = response.xpath("//main[@id='main']")
        headline = response.css('h1.headline-basic::text').getall()
        if main_text_box is not None and len(main_text_box) > 0 and len(headline) > 0:
            all_text = main_text_box[0].css('p::text').getall()
            if len(all_text) > 0:
                # get title
                headline = headline[0]
                # select classes of zn-body__paragraph
                final_text = ''
                for text in all_text:
                    final_text += text
            
                filename = headline.replace(" ", "").replace("\'", "")
                output_name = "Scraped/NJ/" + filename + ".json"
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
