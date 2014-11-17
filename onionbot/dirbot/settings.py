# Scrapy settings for dirbot project
import random

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

DOWNLOAD_TIMEOUT = 120 # 2 min
DOWNLOAD_DELAY = 2 # 2 sec
#DEPTH_LIMIT = 1
DEPTH_STATS = True
DNSCACHE_ENABLED = True
ROBOTSTXT_OBEY = True
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"
CRAWLING_SESSION = str(random.randint(100000, 999999))

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.ProxyMiddleware': 410,
    #'dirbot.middleware.LimitLargeDomains': 411,
    #'dirbot.middleware.IgnoreAlreadyCrawledUrlsMiddleware': 412,
    'dirbot.middleware.SubDomainLimit': 413,
    'dirbot.middleware.FilterBannedDomains': 414,
    'dirbot.middleware.FilterResponses': 999,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
}

#ITEM_PIPELINES = {'dirbot.pipelines.SolrPipeline': 1}

BANNED_DOMAINS = [
    '4006fd82782ad54277439b78ef96f075',
    '642b2830188c780e5b2ed01c07b69a6b',
    'f9ff5c6d6df78cd4ec9592b82e0e18cd',
    '0cb27d976939c444ee644c22af754705',
    'cdc99ab59cb5eb16ddd16ef8bb439cd3',
    '25acdfa56f6a20003763b28e7881ff5a',
    'e2d01757d9b8d81bbb659f807ffec016',
    'b19fb628ff498ad6da4faca70400dfcd',
    'f2ce1f1c2dd8e7622df68c73cf37e262',
    '8cf0505afe29e2457378c965ff8db7c7',
    '2b414e626d3369a3cbc09db841e4ad75',
    'a436778a57e2ae8d0477ee5198391265',
    'e4a82a117460261beae528291a864c13',
    '8d052ff91190018a0f0c655c093e9e14'
    ]

SOLR_CONNECTION = "http://127.0.0.1:8080/solr/" # Connection to Solr
#SOLR_CONNECTION = "http://127.0.0.1:33433/solr/"
MAX_PER_DOMAIN = 100 # Max sites per domain
HTTP_PROXY = "http://localhost:8123/" # HTTP Tor proxy
FRESH_INTERVAL = 30 # Days to pass between re-crawling
