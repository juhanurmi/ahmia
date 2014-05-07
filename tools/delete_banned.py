"""Read all banned domains from ahmia and delete them from YaCy's Solr."""
# -*- coding: utf-8 -*-
from urllib2 import Request
import urllib2
import base64

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
    if not open_connection(req):
        print url

def delete_hidden_services():
    """Delete each banned hidden service from Solr."""
    urldomains = 'https://127.0.0.1/banneddomains.txt'
    links = get2txt(urldomains).split('\n')
    for link in links:
        if not link:
            continue
        print link
        onion_id = link[7:-7]
        url = 'http://10.8.0.10:8080'
        url = url + '/solr/collection1/update?stream.body=<delete><query>host_s:'
        url = url + onion_id + '.onion</query></delete>&commit=true'
        send_get(url)

def get2txt(url):
    """Read text from the URL."""
    txt = ""
    try:
        txt = urllib2.urlopen(url).read()
        return txt
    except urllib2.HTTPError, error:
        print error
        return txt

def main():
    """Main function."""
    delete_hidden_services()

if __name__ == '__main__':
    main()
