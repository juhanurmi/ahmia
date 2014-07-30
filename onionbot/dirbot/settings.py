# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

DOWNLOAD_TIMEOUT = 60 # 1 min
DOWNLOAD_DELAY = 2 # 2 sec
DEPTH_LIMIT = 1
DEPTH_STATS = True
DNSCACHE_ENABLED = True
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.ProxyMiddleware': 410,
    'dirbot.middleware.FilterResponses': 999,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
}
