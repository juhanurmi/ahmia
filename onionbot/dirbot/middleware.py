"""Proxy middleware to support .onion addresses."""

# Install privoxy
#
# sudo nano /etc/privoxy/config
# add one of the following line
# forward-socks5 / 127.0.0.1:9050 .
#
# restart it 
# sudo /etc/init.d/privoxy restart

# Install Tor with Tor2web mode

# Direct every request to .onion sites to privoxy that uses Tor

from urlparse import urlparse

class ProxyMiddleware(object):
    """Middleware for .onion addresses."""
    def process_request(self, request, spider):
	parsed_uri = urlparse( request.url )
	domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	if ".onion" in domain and not ".onion." in domain:
        	request.meta['proxy'] = "http://127.0.0.1:8118"
