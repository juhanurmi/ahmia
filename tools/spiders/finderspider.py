from scrapy import Spider, Request, log
from urllib3 import PoolManager
from items import ToolsItem

class FinderSpider(Spider):
    name = "finderspider"
    allowed_domains = ["deepweblinks.org", "skunksworkedp2cg.tor2web.fi"]
    # TODO: replace default handling for common HTTP error responses (4xx, etc)

    def __init__(self):
        self.onions = set()

    def start_requests(self):
        r1 = Request("http://deepweblinks.org/", callback=self.parse_deepweb)
        #r2 = Request("https://skunksworkedp2cg.tor2web.fi/sites.txt", callback=self.parse_skunksworked)
        r2 = Request("file:///Users/bsloan/Documents/sites.txt", callback=self.parse_skunksworked)
        return [r1, r2]

    def parse_deepweb(self, response):
        scrape = response.selector.xpath("//@href").extract()
        for link in scrape:
            link = link.rstrip("/")
            if ".onion" in link:
                self.log("queued " + link)
                self.onions.add(link)

        self.log("HTTP status 200 received for deepweblinks.org", level=log.INFO)
        self.log("harvested " + str(len(self.onions)) + " .onion links", level=log.INFO)

        item = ToolsItem()  # TODO: actually make a response item??
        return item

    def parse_skunksworked(self, response):
        links = response.body.split('\n')
        for link in links:
            if not link:
                continue
            # abc.something.onion => something
            parts = link.split('.')
            if len(parts) == 2:
                link = "http://" + link
                self.onions.add(link)
            elif len(parts) == 3:
                link = "http://" + parts[1] + ".onion/"
                self.onions.add(link)
            else:
                self.log("failed to queue onion link: " + link, level=log.WARNING)
        item = ToolsItem()
        return item

    def closed(self, reason):
        self.log("\n\n *** finder spider completed ***\n  ", level=log.INFO)
        self.log("number of unique onions queued: " + str(len(self.onions)), level=log.INFO)
        pool = PoolManager()

        for onion in self.onions:
            json = "{\"url\":\"" + onion + "\"}"
            self.log("POSTing onion to ahmia: " + json)

            post_url = "https://ahmia.fi/address/"
            content_type = {"Content-Type": "application/json"}
            req = pool.urlopen("POST", post_url, headers=content_type, body=json)
            if req.status != 200 and req.status != 403:
                self.log("Failed to POST " + onion + " server responded with HTTP " + str(req.status),
                         level=log.ERROR)
