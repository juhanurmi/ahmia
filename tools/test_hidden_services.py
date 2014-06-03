# -*- coding: utf-8 -*-
"""Test all hidden service's: HTTP GET tells if the service is online."""
from urllib2 import Request
import urllib2
import socket
socket.setdefaulttimeout(60)

def open_req(req):
    """Open request."""
    try:
        handle = urllib2.urlopen(req)
        if handle.getcode() != 200:
            print handle.getcode()
        else:
            print handle.read()
            return True
    except urllib2.HTTPError, error:
        print 'HTTPError = ' + str(error.code)
    except urllib2.URLError, error:
        print 'URLError = ' + str(error.reason)
    except Exception:
        import traceback
        print 'generic exception: ' + traceback.format_exc()
    return False

def post(url, data):
    """Send HTTP POST."""
    req = Request(url)
    req.add_data(data)
    req.get_method = lambda: 'POST'
    if not open_req(req):
        print url
        print data

def main():
    """Test each hidden service with HTTP GET."""
    urldomains = 'https://127.0.0.1/alldomains'
    links = get2txt(urldomains).split('\n')
    for link in links:
        if not link:
            continue
        print link
        urlpost = 'https://ahmia.fi/address/'
        hs_id = link[7:-7]
        urlpost = urlpost + hs_id + "/status"
        data = ""
        post(urlpost, data)

def get2txt(url):
    """Read from URL."""
    txt = ""
    try:
        txt = urllib2.urlopen(url).read()
        return txt
    except urllib2.HTTPError, error:
        return txt

if __name__ == '__main__':
    main()

