# -*- coding: utf-8 -*-

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"

SPIDER_MIDDLEWARES = {
    "scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware": 543
}

HTTP_PROXY = "http://127.0.0.1:9050"
HTTPS_PROXY = "http://127.0.0.1:9050"

DOWNLOADER_MIDDLEWARES = {
    'middlewares.ProxyMiddleware': 1
}
