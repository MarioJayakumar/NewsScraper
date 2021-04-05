import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest

class NPRSpider(scrapy.Spider):
    name="NPR"
    start_urls = ["https://www.npr.org/"]

    def start_requests(self):
        yield SeleniumRequest(url=self.start_urls[0], wait_time=3, callback=self.parse)

    def parse(self, response):
        # first check if this is a page
        main_content = response.css("div.storytext")
        all_text = []
        if main_content is not None and len(main_content) > 0:
            all_text = main_content[0].css("p::text").getall()
        if len(all_text) > 0:
            # get title
            headline_div = response.css('div.storytitle')[0]
            headline = headline_div.css('h1::text').getall()
            headline = headline[0]
            # select classes of zn-body__paragraph
            final_text = ''
            for text in all_text:
                final_text += text
        
            filename = headline.replace(" ", "").replace("\'", "")
            output_name = "Scraped/NPR/" + filename + ".json"
            output_json = {}
            output_json["title"] = headline
            output_json["body"] = final_text
            with open(output_name, "w+") as output_fh:
                json.dump(output_json, output_fh)

        # follow links in page
        link_subset = response.xpath("//section[@id='main-section']")
        if len(link_subset) > 0:
            for link in link_subset[0].xpath("//a/@href").getall():
                link = response.urljoin(link)
                if link.startswith(response.url):
                    yield SeleniumRequest(url=link, wait_time=3, callback=self.parse)
