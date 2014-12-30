import codecs
import json
from re import match
from datetime import datetime
from scrapy import Spider, log
from items import ToolsItem

class T2WDomainSpider(Spider):
    name = "t2w_domain_spider"
    nodes = ["tor2web.fi", "tor2web.org", "onion.to", "tor2web.blutmagie.de", "onion.lt", "onion.cab", "onion.lu"]
    start_urls = ["https://abcd." + node + "/antanistaticmap/stats/yesterday" for node in nodes]

    def parse(self, response):
        timestamp = datetime.now().strftime("%y-%m-%d-%H-%M")
        try:
            node = match(r"(http.*abcd\.)(.+?/)", response.url).group(2)  # gets the domain
            if node:
                node = node.replace(".", "").replace("/", "_")
                filename = "/usr/local/lib/ahmia/tor2web_stats/" + node + timestamp + ".json"
                json_str = valid_pretty_json(response.body)
                text2file(json_str, filename)
            else:
                raise Exception
        except Exception as exc:  # catch all
            self.log("Failed to save json data for " + response.url, level=log.ERROR)
            print exc

        item = ToolsItem()
        return item


# utility methods from the original script

def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()


def valid_pretty_json(myjson):
    """Check that text string is valid JSON."""
    parsed = json.loads(myjson)
    return json.dumps(parsed, indent=4, sort_keys=True, ensure_ascii=False)
