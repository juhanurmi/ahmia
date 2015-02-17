from scrapy import Spider, Request, log
import urllib2
import signal

class TestHiddenServiceSpider(Spider):
    name = "test_services_spider"

    def start_requests(self):
        # serves a plain text, line-delimited list of onions to check
        return [Request("https://127.0.0.1:45454/alldomains", callback=self.parse_list)]

    def parse_list(self, response):
        self.log("Parsing onion list from " + response.url, level=log.INFO)
        links = response.body.split('\n')
        return [Request(link, callback=self.check_onion) for link in links if link]

    def check_onion(self, response):
        self.log("Checked onion " + response.url)

        # scrape the metadata from html response
        title_element = response.selector.xpath("//title/text()").extract()
        h1_element = response.selector.xpath("//h1/text()").extract()
        desc_element = response.selector.xpath("//*[@name='description']/@content").extract()
        keywords_element = response.selector.xpath("//*[@name='keywords']/@content").extract()

        # parsing logic for descriptive metadata is from the original script (test_hidden_services.py):
        title = ""
        keywords = ""
        description = ""
        if len(title_element) > 0:
            title = title_element[0]
        if len(desc_element) > 0:
            description = desc_element[0]
        if len(keywords_element) > 0:
            keywords = keywords_element[0]
        if not title and len(h1_element) > 0:
            title = h1_element[0]
        if title or keywords or description:
            json_data = '{"not_official": 1, "title": "'
            json_data = json_data + title[:100] + '", "description": "'
            json_data = json_data + description[:500] + '", "relation": "",'
            json_data = json_data + '"keywords": "' + keywords[:200]
            json_data = json_data + '", "type": "", "language": "",'
            json_data = json_data + '"contactInformation": "" }'

            # PUT the json to ahmia endpoint
            send_put("https://127.0.0.1:45454/address/", json_data)
        else:
            self.log("Failed to extract descriptive metadata from onion: " + response.url, level=log.WARNING)


# utilities from the original script
class Timeout(object):
    """Timeout class using ALARM signal"""
    class Timeout(Exception):
        """Pass exception."""
        pass
    def __init__(self, sec):
        """Init."""
        self.sec = sec
    def __enter__(self):
        """ALARM signal."""
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
    def __exit__(self, *args):
        """Disable alarm."""
        signal.alarm(0)
    def raise_timeout(self, *args):
        """Timeout."""
        raise Timeout.Timeout()


def open_req(req):
    """Open request."""
    try:
        # Run block of code with timeouts
        with Timeout(60):
            handle = urllib2.urlopen(req)
        if handle.getcode() != 200:
            print handle.getcode()
            handle.close()
        else:
            print handle.read()
            handle.close()
            return True
    except Timeout.Timeout:
        print "Timeout"
    except urllib2.HTTPError, error:
        print 'HTTPError = ' + str(error.code)
    except urllib2.URLError, error:
        print 'URLError = ' + str(error.reason)
    except Exception:
        import traceback
        print 'generic exception: ' + traceback.format_exc()
    return False


def send_put(url, data):
    """Send HTTP PUT"""
    req = urllib2.Request(url)
    req.add_data(data)
    req.get_method = lambda: 'PUT'
    if not open_req(req):
        print "Updating failed:"
        print url
        print data
