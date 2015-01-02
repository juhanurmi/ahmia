from scrapy import Spider, log
from re import match
import codecs

class T2WFilterSpider(Spider):
    name = "t2w_filter_spider"
    nodes = ["tor2web.fi", "tor2web.org", "onion.to", "tor2web.blutmagie.de", "onion.lt", "onion.cab", "onion.lu"]
    start_urls = ["https://abcd." + node + "/antanistaticmap/lists/blacklist" for node in nodes]

    def parse(self, response):
        try:
            filename = "../ahmia/static/log/"
            node = match(r"(http.*abcd\.)(.+?/)", response.url).group(2)  # gets the domain
            if node:
                filename = filename + node.rstrip("/") + "_md5filterlist.txt"
                text2file(response.body, filename)
            else:
                raise Exception
        except Exception as exc:  # catch all
            self.log("Failed to save data for " + response.url, level=log.ERROR)
            print exc


# utility methods from the original script
# TODO: would be nice to move these and other reused util methods to a separate module

def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()
