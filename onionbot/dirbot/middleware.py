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

import re
from urlparse import urlparse

from scrapy import log
from scrapy.exceptions import IgnoreRequest


class ProxyMiddleware(object):
    """Middleware for .onion addresses."""
    def process_request(self, request, spider):
        parsed_uri = urlparse( request.url )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if ".onion" in domain and not ".onion." in domain:
            request.meta['proxy'] = "http://localhost:8118"



# Middleware to exclude any response type that isn't in a whitelist


class FilterResponses(object):
    """Limit the HTTP response types that Scrapy dowloads."""

    @staticmethod
    def is_valid_response(type_whitelist, content_type_header):
        for type_regex in type_whitelist:
            if re.search(type_regex, content_type_header):
                return True
        return False


    def process_response(self, request, response, spider):
        """
        Only allow HTTP response types that that match the given list of
        filtering regexs
        """
        # to specify on a per-spider basis
        # type_whitelist = getattr(spider, "response_type_whitelist", None)
        type_whitelist = (r'text', )
        content_type_header = response.headers.get('content-type', None)
        if content_type_header and self.is_valid_response(type_whitelist, content_type_header):
            return response
        else:
            msg = "Ignoring request {}, content-type was not in whitelist".format(response.url)
            log.msg(msg, level=log.INFO)
            raise IgnoreRequest()
