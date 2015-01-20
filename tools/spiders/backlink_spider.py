from scrapy import Spider
from scrapy import log
from items import ToolsItem

class BacklinkSpider(Spider):
    name = "backlink_spider"
    allowed_domains = ["startpage.com"]

    def __init__(self, target="", host=None, links=None, count=None):
        start_page_search = """https://startpage.com/do/search
        ?cmd=process_search&language=english&enginecount=1&pl=&abp=
        1&cdm=&tss=1&ff=&theme=&prf=464341bcfbcf47b736ff43307aef287a
        &suggestOn=1&flag_ac=0&lui=english&cat=web&query="""
        start_page_search = start_page_search.replace("\n", "")
        start_page_search = start_page_search.replace(" ", "")

        if host:
            start_page_search = start_page_search + "host%3A" + host + "+"
        else:
            host = "ANY"

        start_page_search = start_page_search + "link%3A" + target
        if not links:
            start_page_search = start_page_search.replace("link%3A", "")

        self.start_urls = [start_page_search]
        self.count = count
        self.target = target
        self.host = host
        self.links = links

    def parse(self, response):
        if response.status == 200:
            links_count = ""
            scrape = response.selector.xpath("//p[@id='results_count_p']/text()").extract()
            if len(scrape) > 0:
                links_count = find_between(scrape[0], "About ", " results")

            if self.count:
                self.count = links_count

            self.backlinks = \
                [link for link in response.selector.xpath("//h3//a/@href").extract()
                 if not "http://www.google.com/" in link]

        else:
            self.log("backlink spider received HTTP response status {0}"
                     .format(response.status), level=log.WARNING)

        item = ToolsItem()  # TODO: actually make a backlinker response item??
        return item

    def closed(self, reason):
        self.log("\n\n *** backlink spider completed ***\n  " +
                 "target site={0}\n  host={1}\n  links={2}\n  backlink count={3}\n"
                 .format(self.target, self.host, self.links, self.count), level=log.INFO)

        if not self.count:
            result_string = ""
            for link in self.backlinks:
                result_string += link + "\n"
            self.log("The most relevant results are shown (some entries are omitted):\n\n" + result_string,
                     level=log.INFO)
        else:  # prints the count as integer to stdout as expected by existing tools. useful if logging is disabled
            print self.count


def find_between(string, first, last):
    """Return substring between 'first' and 'last'."""
    try:
        start = string.index(first) + len(first)
        end = string.index(last, start)
        return string[start:end]
    except ValueError:
        return ""
