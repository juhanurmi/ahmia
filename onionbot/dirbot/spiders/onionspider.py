# -*- coding: UTF-8 -*-

import re

import html2text
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from dirbot.items import CrawledWebsiteItem


class OnionSpider(CrawlSpider):
    name = "OnionSpider"
    allowed_domains = ["onion"]
    start_urls = [
        "https://ahmia.fi/address/",
    ]

    rules = (
        Rule (SgmlLinkExtractor(), callback="parse_items", follow= True),
    )

    def detect_encoding(self, response):
        return response.headers.encoding or "utf-8"

    def html2string(self, response):
        """HTML 2 string converter. Returns a string."""
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        encoding = self.detect_encoding(response)
        decoded_html = response.body.decode(encoding, 'ignore')
        string = converter.handle(decoded_html)
        return string

    def extract_words(self, html_string):
        """Stems and counts the words. Works only in English!"""
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

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = CrawledWebsiteItem()
        item['url'] = response.url
        title_list = hxs.xpath('//title/text()').extract()
        title = ' '.join(title_list)
        item['title'] = title
        body_text = self.html2string(response)
        words = self.extract_words(body_text)
        item['text'] = title + " " + " ".join(words)
        return item
