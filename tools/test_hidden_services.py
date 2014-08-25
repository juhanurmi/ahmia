# -*- coding: utf-8 -*-
"""Test all hidden service's: HTTP GET tells if the service is online."""
import httplib
import signal  # To timeout the TCP/HTTP connection
import socket
import time
import urllib2
from urllib2 import Request

import simplejson
import socks
from bs4 import BeautifulSoup  # To parse HTML

socket.setdefaulttimeout(80) # Timeout after 1min 20s

class SocksiPyConnection(httplib.HTTPConnection):
    """Socks connection for HTTP."""
    def __init__(self, proxytype, proxyaddr, proxyport=None, rdns=True,
    username=None, password=None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns,
        username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)
    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

class SocksiPyHandler(urllib2.HTTPHandler):
    """Socks connection for HTTP."""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)
    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            """Build connection."""
            conn = SocksiPyConnection(*self.args, host=host, port=port,
            strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)

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
    """Send HTTP POST."""
    req = Request(url)
    req.add_data(data)
    req.get_method = lambda: 'PUT'
    if not open_req(req):
        print url
        print data

def main():
    """Test each hidden service with HTTP GET."""
    urldomains = 'https://127.0.0.1:45454/alldomains'
    links = get2txt(urldomains).split('\n')
    for link in links:
        if not link:
            continue
        print link
        put_url = 'https://127.0.0.1:45454/address/'
        hs_id = link[7:-7]
        put_url = put_url + hs_id + "/status"
        data = hs_online_check(hs_id)
        send_put(put_url, data)

def get2txt(url):
    """Read from URL."""
    txt = ""
    try:
        txt = urllib2.urlopen(url).read()
        return txt
    except urllib2.HTTPError:
        return txt

def hs_online_check(onion):
    """Online check for hidden service."""
    try:
        return hs_http_checker(onion)
    except Exception as error:
        print error
        return ""

def hs_http_checker(onion):
    """Socks connection to the Tor network. Try to download an onion."""
    socks_con = SocksiPyHandler(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', 9050)
    opener = urllib2.build_opener(socks_con)
    return hs_downloader(opener, onion)

def hs_downloader(opener, onion):
    """Try to download the front page and description.json."""
    handle = opener.open('http://'+str(onion)+'.onion/')
    code = handle.getcode()
    print "Site answers to the online check with code %d." % code
    if code != 404: # It is up
        json_html = analyze_front_page(handle.read(), onion)
        json_official = hs_download_description(opener, onion)
        if json_official:
            json_data = json_official
        else:
            json_data = json_html
        return json_data
    else:
        return ""

def analyze_front_page(raw_html, onion):
    """Analyze raw HTML page."""
    try:
        soup = BeautifulSoup(raw_html)
        title_element = soup.find('title')
        desc_element = soup.find(attrs={"name":"description"})
        keywords_element = soup.find(attrs={"name":"keywords"})
        title = ""
        keywords = ""
        description = ""
        h1_element = soup.find('h1')
        if title_element:
            title = title_element.string.encode('utf-8')
        if desc_element and desc_element['content']:
            description = desc_element['content'].encode('utf-8')
        if keywords_element and keywords_element['content']:
            keywords = keywords_element['content'].encode('utf-8')
        if not title and h1_element:
            title = h1_element.string.encode('utf-8')
        if title or keywords or description:
            json_data = '{"not_official": 1, "title": "'
            json_data = json_data + title[:100] + '", "description": "'
            json_data = json_data + description[:500] + '", "relation": "",'
            json_data = json_data + '"keywords": "' + keywords[:200]
            json_data = json_data + '", "type": "", "language": "",'
            json_data = json_data + '"contactInformation": "" }'
            return json_data
        else:
            return ""
    except:
        return ""

def hs_download_description(opener, onion):
    """Try to download description.json."""
    try:
        dec_url = 'http://'+str(onion)+'.onion/description.json'
        handle = opener.open(dec_url)
        descr = handle.read()
        # There cannot be that big descriptions
        if len(descr) < 5000:
            descr = descr.replace('\r', '')
            descr = descr.replace('\n', '')
            simplejson.loads(descr)
            return descr
    except:
        return ""

if __name__ == '__main__':
    main()
