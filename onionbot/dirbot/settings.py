# Scrapy settings for dirbot project
import random  # To generate crawling session ID

import requests  # To fetch the list of banned domains

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

DOWNLOAD_TIMEOUT = 120 # 2 min
DOWNLOAD_DELAY = 2 # 2 sec
DEPTH_LIMIT = 1
DEPTH_STATS = True
DNSCACHE_ENABLED = True
ROBOTSTXT_OBEY = True
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"
CRAWLING_SESSION = str(random.randint(100000, 999999))

# Search engine point of view
CONCURRENT_REQUESTS = 10
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
RETRY_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.ProxyMiddleware': 410,
    #'dirbot.middleware.LimitLargeDomains': 411,
    #'dirbot.middleware.IgnoreAlreadyCrawledUrlsMiddleware': 412,
    'dirbot.middleware.LimitDomainsPerCrawl': 413,
    'dirbot.middleware.SubDomainLimit': 414,
    #'dirbot.middleware.FilterBannedDomains': 415,
    'dirbot.middleware.FilterResponses': 999,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
}

ITEM_PIPELINES = {'dirbot.pipelines.SolrPipeline': 1}

BANNED_DOMAINS = []

response = requests.get('https://ahmia.fi/banned/')
for md5 in response.text.split("\n"):
    if len(md5) is 32:
        BANNED_DOMAINS.append(md5)

SOLR_CONNECTION = "http://127.0.0.1:8080/solr/" # Connection to Solr
MAX_PER_DOMAIN = 1000 # Max sites per domain
HTTP_PROXY = "http://localhost:8123/" # HTTP Tor proxy
FRESH_INTERVAL = 30 # Days to pass between re-crawling
