# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

DOWNLOAD_TIMEOUT = 60 # 1 min
DOWNLOAD_DELAY = 2 # 2 sec
#DEPTH_LIMIT = 1
DEPTH_STATS = True
DNSCACHE_ENABLED = True
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.ProxyMiddleware': 410,
    #'dirbot.middleware.LimitLargeDomains': 411,
    #'dirbot.middleware.IgnoreAlreadyCrawledUrlsMiddleware': 412,
    'dirbot.middleware.SubDomainLimit': 413,
    'dirbot.middleware.FilterResponses': 999,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
}

ITEM_PIPELINES = {'dirbot.pipelines.SolrPipeline': 1}

BANNED_DOMAINS = [
    '4006fd82782ad54277439b78ef96f075',
    '6b29b723fdf806c98304d5866c8b934e',
    'a679199f86a83b87723ae433882b6706',
    'f2ce1f1c2dd8e7622df68c73cf37e262',
    '90644230609136d433cc5a11003932e9',
    '54571a890aa1666ed3f822226716675c',
    '4c15832d6f1539835dee2244da98c3c1',
    '725229a4fa42f3596673d3831508e4b9',
    '8d052ff91190018a0f0c655c093e9e14'
    ]

SOLR_CONNECTION = "http://127.0.0.1:8080/solr/" # Connection to Solr
MAX_PER_DOMAIN = 1000 # Max sites per domain
HTTP_PROXY = "http://localhost:8123/" # HTTP Tor proxy
FRESH_INTERVAL = 7 # Days to pass between re-crawling
