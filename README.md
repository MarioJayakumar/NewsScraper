# NewsScraper Project


## Usage

A selenium chromedriver is required to run the spiders. The driver must be stored in newsscraper/newsscraper/chromedriver

## Spiders

As of now, these are the implemented spiders, each for scraping the respective site.

Spiders:

ABCSpider-> ABC Go News

BaltimoreFishbowlSpider -> baltimorefishbowl.com

CNNSpider -> cnn.com

NJSpider -> nj.com

NPRSpider -> npr.org


The spider crawling policy is fairly straightforward. Any hyperlinks on a webpage are recursively explored. If a visited page is an article, the text content of the page is saved to a json file. The json file will have a file name which matches the article title, and the article title and article text are stored in the json.

## Spider Issues

Captured text is not sanitized, file titles can be poorly formatted

Scrapy spiders are started via driver script, can probably utilize scrapy built in methods instead

Along with scraped news articles, non-news articles like privacy policies and terms of use are scraped

No resource limits enforced on spiders while crawling

Pretty poor code quality