"""Use the data from Tor2web nodes."""
# -*- coding: utf-8 -*-
import urllib3 #To HTTP requests
from bs4 import BeautifulSoup # To parse HTML

def load_adapters():
    """Call all the URL find adapters."""
    # http://deepweblinks.org/
    if deepweblinks():
        print "Downloaded a list from skunksworkedp2cg.onion"
    else:
        print "Failed to download from skunksworkedp2cg.onion"
    # http://skunksworkedp2cg.onion/
    if skunksworked():
        print "Downloaded a list from skunksworkedp2cg.onion"
    else:
        print "Failed to download from skunksworkedp2cg.onion"

def deepweblinks():
    """ Download an onion list form http://deepweblinks.org/"""
    pool = urllib3.PoolManager()
    urldomains = 'http://deepweblinks.org/'
    req = pool.request('GET', urldomains)
    if req.status != 200:
        print req.status
        return False
    links = []
    soup = BeautifulSoup(req.data)
    for a_element in soup.find_all('a', href=True):
        url = a_element['href']
        if url and ".onion" in url:
            url = url.replace('http://', '')
            url = url[0:16]
            links.append(url)
    for link in links:
        data = '{"url":"http://' + link + '.onion/"}'
        post_url = 'https://ahmia.fi/address/'
        content_type = {'Content-Type':'application/json'}
        req = pool.urlopen('POST', post_url, headers=content_type, body=data)
        if req.status != 200 and req.status != 403:
            print "Failed to add "+link
    return True

def skunksworked():
    """ Download an onion list form skunksworkedp2cg.onion"""
    pool = urllib3.PoolManager()
    urldomains = 'https://skunksworkedp2cg.tor2web.fi/sites.txt'
    req = pool.request('GET', urldomains)
    if req.status != 200:
        print req.status
        return False
    links = req.data.split('\n')
    for link in links:
        if not link:
            continue
        # abc.something.onion => something
        parts = link.split('.')
        if len(parts) == 2:
            data = '{"url":"http://' + link + '/"}'
        elif len(parts) == 3:
            data = '{"url":"http://' + parts[1] + '.onion/"}'
        else:
            print "Failed to add "+link
            continue
        post_url = 'https://ahmia.fi/address/'
        content_type = {'Content-Type':'application/json'}
        req = pool.urlopen('POST', post_url, headers=content_type, body=data)
        if req.status != 200 and req.status != 403:
            print "Failed to add "+link
    return True

def main():
    """Main."""
    load_adapters()

if __name__ == '__main__':
    main()
