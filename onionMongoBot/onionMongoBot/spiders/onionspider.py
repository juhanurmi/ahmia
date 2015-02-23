# -*- coding: UTF-8 -*-

from urlparse import urlparse

import scrapy
from scrapy.conf import settings
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from onionMongoBot.items import CrawledWebsiteItem


class OnionSpider(CrawlSpider):
    name = "OnionSpider"
    allowed_domains = ["onion"]
    start_urls = settings.get('TARGET_SITES')

    rules = (Rule(SgmlLinkExtractor(), callback='parse', follow=False), )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = CrawledWebsiteItem()
        item['url'] = response.url
        # Add the domain
        domain = urlparse( item['url'] ).hostname
        item['domain'] = domain
        title_list = hxs.xpath('//title/text()').extract()
        h1_list = hxs.xpath("//h1/text()").extract()
        item['h1'] = " ".join(h1_list)
        h2_list = hxs.xpath("//h2/text()").extract()
        item['h2'] = " ".join(h2_list)
        title = ' '.join(title_list)
        item['title'] = title
        item['html'] = response
        return item
