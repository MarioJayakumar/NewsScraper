# NewsScraper Dashboard


## Usage

A selenium chromedriver is required to run the spiders. The driver must be stored in newsscraper/newsscraper/chromedriver

In order to run the spiders continuously, the command `python3 run_continuous.py` can be called. This will start the spiders at 10:00 AM and 10:00 PM every day and let them run for 90 minutes. 

## Spiders

As of now, these are the implemented spiders, each for scraping the respective site.

Spiders:

ABCSpider-> ABC Go News

AfroSpider -> afro.com

BaltimoreFishbowlSpider -> baltimorefishbowl.com

BaltimoreJewishTimesSpider -> www.jewishtimes.com

FoxBaltimoreSpider -> www.foxbaltimore.com

CNNSpider -> cnn.com

NBCPGSpider -> www.nbcwashington.com/news/local/prince-georges-county/

NJSpider -> nj.com

NPRSpider -> npr.org

PGPDSpider -> pgpolice.blogspot.com

WBALTVSpider -> www.wbaltv.com

WJLASpider -> wjla.com

WJZSpider -> baltimore.cbslocal.com

WKYTSpider -> www.wkyt.com

WMARSpider -> www.wmar2news.com/news/


