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
    '642b2830188c780e5b2ed01c07b69a6b',
    'cdc99ab59cb5eb16ddd16ef8bb439cd3',
    '25acdfa56f6a20003763b28e7881ff5a',
    'e2d01757d9b8d81bbb659f807ffec016',
    'b19fb628ff498ad6da4faca70400dfcd',
    'f2ce1f1c2dd8e7622df68c73cf37e262',
    '8d052ff91190018a0f0c655c093e9e14'
    ]

SOLR_CONNECTION = "http://127.0.0.1:8080/solr/" # Connection to Solr
MAX_PER_DOMAIN = 1000 # Max sites per domain
HTTP_PROXY = "http://localhost:8123/" # HTTP Tor proxy
FRESH_INTERVAL = 7 # Days to pass between re-crawling
