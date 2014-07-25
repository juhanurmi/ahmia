# -*- coding: UTF-8 -*-

import os
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
        "http://deepweblinks.org/",
        "https://skunksworkedp2cg.tor2web.fi/",

    ]

    rules = (
        Rule (SgmlLinkExtractor(), callback="parse_items", follow= True),
    )

    file_name = os.path.dirname(os.path.abspath(__file__)) + "/stemmed_stopwords.txt"

    with open(file_name) as file:
        stopwords = file.readlines()

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
        words = []
        for word in string_list:
	    # Word must be longer than 1 letter
	    # And shorter than 45
        # The longest word in a major dictionary is
	    # Pneumonoultramicroscopicsilicovolcanoconiosis (45 letters)
            if len(word) > 1 and len(word) <= 45:
                word = word.lower()
                test_word = word + "\n"
                if not test_word in self.stopwords:
                    words.append(word)
        return words

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = CrawledWebsiteItem()
        item['id'] = response.url
        item['title'] = hxs.xpath('//title/text()').extract()
        body_text = self.html2string(response)
        words = self.extract_words(body_text)
        item['text'] = words
        return item
