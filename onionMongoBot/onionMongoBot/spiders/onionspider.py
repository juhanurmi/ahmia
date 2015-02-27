# -*- coding: UTF-8 -*-

import re
from urlparse import urlparse

import html2text
import scrapy
from scrapy.conf import settings
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from onionMongoBot.items import CrawledWebsiteItem


class OnionSpider(CrawlSpider):
    name = "OnionSpider"
    allowed_domains = ["onion"]
    start_urls = settings.get('TARGET_SITES')

    rules = (Rule(LinkExtractor(), callback='parse_item', follow=True), )

    def parse_item(self, response):
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
        encoding = self.detect_encoding(response)
        decoded_html = response.body.decode(encoding, 'ignore')
        item['html'] = decoded_html
        html_text = self.html2string(decoded_html)
        words = self.extract_words(html_text)
        item['words'] = title + " " + " ".join(words)
        return item

    def detect_encoding(self, response):
        return response.headers.encoding or "utf-8"

    def html2string(self, decoded_html):
        """HTML 2 string converter. Returns a string."""
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        string = converter.handle(decoded_html)
        return string

    def extract_words(self, html_string):
        """Create a word list."""
        string_list = re.split(r' |\n|#|\*', html_string)
        # Cut a word list that is larger than 10000 words
        if len(string_list) > 10000:
            string_list = string_list[0:10000]
        words = []
        for word in string_list:
            # Word must be longer than 0 letter
            # And shorter than 45
            # The longest word in a major English dictionary is
            # Pneumonoultramicroscopicsilicovolcanoconiosis (45 letters)
            if len(word) > 0 and len(word) <= 45:
                words.append(word)
        return words
