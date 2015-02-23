"""Proxy middleware to support .onion addresses."""

# Install Polipo
# and setup Polipo http://localhost:8123/

# Install Tor with Tor2web mode

# Direct every request to .onion sites to privoxy that uses Tor

from urlparse import urlparse

from scrapy.conf import settings


class ProxyMiddleware(object):
    """Middleware for .onion addresses."""
    def process_request(self, request, spider):
        parsed_uri = urlparse( request.url )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if ".onion" in domain and not ".onion." in domain:
            request.meta['proxy'] = settings.get('HTTP_PROXY')
