"""Read hidden service domains from YaCy's Solr."""
# -*- coding: utf-8 -*-
from urllib2 import Request
import urllib2
import base64
import xml.etree.ElementTree as ET #XML
import re

def validate_onion_url(url):
    """Test that the URL a valid onion URL."""
    # Must be like http://3g2upl4pq6kufc4m.onion/
    if len(url) != 30:
        return False
    if url[0:7] != 'http://':
        return False
    if url[-7:] != '.onion/':
        return False
    if not re.match("[a-z2-7]{16}", url[7:-7]):
        return False
    return True

def open_connection(req):
    """Request handler."""
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

def auth(req):
    """Basic authentication."""
    #BASE64_CREDENTIALS=$(echo -n "<username>:<password>" | base64)
    #curl -i --header "Authorization:Basic ${BASE64_CREDENTIALS}" <url>
    username = 'solr-access'
    password = 'E51Zs9l9Gfd7kzN67v9OldTEVw'
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    header = "Basic %s" % base64string
    req.add_header("Authorization", header)

def send_get(url):
    """Authenticate and send GET request to the URL."""
    req = Request(url)
    auth(req)
    result = open(req)
    if not result:
        print "Error..."
        return ""
    return result

def add_hidden_services(start):
    """Print a list of hidden services from Solr."""
    found = False
    start_str = '%d' % start
    urldomains = 'http://10.8.0.10:8080/solr/select?q=host_s:*&defType=edismax&start='+start_str+'&core=collection1&fl=host_s&rows=10100'
    xml_string = send_get(urldomains)
    try:
        root = ET.fromstring(xml_string) #<response>
        result = root.find('result') #<result>
        for doc in result.findall('doc'):
            for string in doc.findall('str'):
                if "host_s" in string.get('name'):
                    domain = "http://"+string.text+"/"
                    if validate_onion_url(domain):
                        print '{"url":"'+domain+'"}'
                        found = True
    except:
        print xml_string
    return found

def main():
    """Main function."""
    start = 0
    while True:
        if not add_hidden_services(start):
            break
        start = start + 10000

if __name__ == '__main__':
    main()
