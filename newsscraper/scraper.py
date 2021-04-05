import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from newsscraper.spiders.CNNSpider import CNNSpider
from newsscraper.spiders.ABCSpider import ABCSpider
from newsscraper.spiders.BaltimoreFishbowlSpider import BaltimoreFishbowlSpider
from newsscraper.spiders.NJSpider import NJSpider
from newsscraper.spiders.NPRSpider import NPRSpider
from scrapy.utils.project import get_project_settings
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--spider", default="CNN", help="Which spider to use. Options are [ABC, BaltimoreFishbowl, CNN, NJ, NPR]")
    args = parser.parse_args()
    spider_name = args.spider

    process = CrawlerProcess(get_project_settings())

    if spider_name == "ABC":
        process.crawl(ABCSpider)
    elif spider_name == "BaltimoreFishbowl":
        process.crawl(BaltimoreFishbowlSpider)
    elif spider_name == "CNN":
        process.crawl(CNNSpider)
    elif spider_name == "NJ":
        process.crawl(NJSpider)
    elif spider_name == "NPR":
        process.crawl(NPRSpider)
    process.start()