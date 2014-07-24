# -*- coding: UTF-8 -*-

import os
import re

import html2text
from nltk.stem import PorterStemmer
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from urlparse import urlparse

from dirbot.items import Website

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
        decoded_html = response.body.decode(encoding)
        string = converter.handle(decoded_html)
	return string

    def word_count(self, string):
	"""Stems and counts the words. Works only in English!"""
        string = re.split(r' |\n|#|\*', string)
        words = {}
        port = PorterStemmer()
        for word in string:
	    # Word must be longer than 1 letter 
	    # And shorter than 45
            # The longest word in a major dictionary is 
	    # Pneumonoultramicroscopicsilicovolcanoconiosis (45 letters)
            if len(word) > 1 and len(word) < 45:
                word = word.lower()
                word = port.stem(word)
                if word in words:
                    words[word] = words[word] + 1
                else:
                    test_word = word + "\n"
                    if not test_word in self.stopwords:
                        words[word] = 1
        return words

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = Website()
        parsed_uri = urlparse( response.url )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        item['domain'] = domain
        item['url'] = response.url
        item ['title'] = hxs.xpath('//title/text()').extract()
        item['keywords'] = hxs.xpath('//keywords/text()').extract()
        item['h1'] = hxs.xpath('//h1/text()').extract()
        item['h2'] = hxs.xpath('//h2/text()').extract()
        item['h3'] = hxs.xpath('//h3/text()').extract()
        item['h4'] = hxs.xpath('//h1/text()').extract()
	body_text = self.html2string(response)
	item['text'] = body_text
        item['words'] = self.word_count(body_text)
        return item
