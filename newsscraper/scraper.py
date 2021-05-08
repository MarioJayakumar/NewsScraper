import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
from scrapy_selenium import SeleniumRequest
from newsscraper.spiders.CNNSpider import CNNSpider
from newsscraper.spiders.ABCSpider import ABCSpider
from newsscraper.spiders.BaltimoreFishbowlSpider import BaltimoreFishbowlSpider
from newsscraper.spiders.NBC_PGSpider import NBC_PGSpider
from newsscraper.spiders.NJSpider import NJSpider
from newsscraper.spiders.NPRSpider import NPRSpider
from newsscraper.spiders.PGPDSpider import PGPDSpider
from newsscraper.spiders.WJLASpider import WJLASpider
from newsscraper.spiders.WKYTSpider import WKYTSpider
from newsscraper.spiders.WTOP_PGSpider import WTOP_PGSpider
from newsscraper.spiders.FoxBaltimoreSpider import FoxBaltimoreSpider
from newsscraper.spiders.WBALTVSpider import WBALTVSpider
from newsscraper.spiders.WJZSpider import WJZSpider
from newsscraper.spiders.WMARSpider import WMARSpider
from scrapy.utils.project import get_project_settings
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--spider", default="all", help="Which spider to use. Options are [all, ABC, BaltimoreFishbowl, FoxBaltimore, CNN, NJ, NPR, WBALTV, WJLA, WJZ, WKYT, WMAR]. If all selected, then all scrapers run.")
    args = parser.parse_args()
    spider_name = args.spider

    

    if spider_name != "all":
        process = CrawlerProcess(get_project_settings())
        if spider_name == "ABC":
            process.crawl(ABCSpider)
        elif spider_name == "BaltimoreFishbowl":
            process.crawl(BaltimoreFishbowlSpider)
        elif spider_name == "FoxBaltimoreFishbowl":
            process.crawl(FoxBaltimoreSpider)            
        elif spider_name == "CNN":
            process.crawl(CNNSpider)
        elif spider_name == "NJ":
            process.crawl(NJSpider)
        elif spider_name == "NPR":
            process.crawl(NPRSpider)
        elif spider_name == "WBALTV":
            process.crawl(WBALTVSpider)
        elif spider_name == "WJLA":
            process.crawl(WJLASpider)
        elif spider_name == "WJZ":
            process.crawl(WJZSpider)            
        elif spider_name == "WKYT":
            process.crawl(WKYTSpider)     
        elif spider_name == "WMAR":
            process.crawl(WMARSpider)                   
        else:
            print("Unknown spider passed")
        process.start()
    else:
        process = CrawlerProcess(get_project_settings())
        process.crawl(ABCSpider)
        process.crawl(BaltimoreFishbowlSpider)
        process.crawl(FoxBaltimoreSpider)
        process.crawl(CNNSpider)
        process.crawl(NBC_PGSpider)
        process.crawl(NJSpider)
        process.crawl(NPRSpider)
        process.crawl(PGPDSpider)
        process.crawl(WBALTVSpider)
        process.crawl(WJLASpider)
        process.crawl(WJZSpider)
        process.crawl(WKYTSpider)
        process.crawl(WMARSpider)
        process.crawl(WTOP_PGSpider)
        process.start()
