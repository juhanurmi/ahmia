# -*- coding: utf-8 -*-

NAME = 'backlinkspider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"

SPIDER_MIDDLEWARES = {
    "scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware": 543
}
