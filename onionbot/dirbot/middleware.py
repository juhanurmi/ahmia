"""Proxy middleware to support .onion addresses."""

# Install Polipo
# and setup Polipo http://localhost:8123/

# Install Tor with Tor2web mode

# Direct every request to .onion sites to privoxy that uses Tor

import datetime
import hashlib
import re
from urlparse import urlparse

import pysolr
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import IgnoreRequest


class FilterBannedDomains(object):
    """
    Middleware to filter requests to banned domains.
    """
    def process_request(self, request, spider):
        parsed_uri = urlparse(request.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        domain = domain.replace("http://", "").replace("https://", "").replace("/", "")
        banned_domains = settings.get('BANNED_DOMAINS')
        if hashlib.md5(domain).hexdigest() in banned_domains:
            # Do not execute this request
            request.meta['proxy'] = ""
            msg = "Ignoring request {}, This domain is banned.".format(request.url)
            log.msg(msg, level=log.INFO)
            raise IgnoreRequest()

class LimitDomainsPerCrawl(object):
    """
    Middleware to limit the number of request to large sites per crawling session.
    """
    def process_request(self, request, spider):
        hostname = urlparse(request.url).hostname
        solr = pysolr.Solr(settings.get('SOLR_CONNECTION'), timeout=10)
        query = 'domain:*' + hostname.split(".")[-2] + '.onion*'
        query = query + " AND crawling_session:" + settings.get('CRAWLING_SESSION')
        if solr.search(query).hits > settings.get('MAX_PER_DOMAIN'):
            # Do not execute this request
            request.meta['proxy'] = ""
            msg = "Ignoring request {}, More than 1000 sites crawled from this domain.".format(request.url)
            log.msg(msg, level=log.INFO)
            raise IgnoreRequest()

class LimitLargeDomains(object):
    """
    Middleware to limit the number of request to large sites.
    """
    def process_request(self, request, spider):
        hostname = urlparse(request.url).hostname
        solr = pysolr.Solr(settings.get('SOLR_CONNECTION'), timeout=10)
        query = 'domain:*' + hostname.split(".")[-2] + '.onion*'
        if solr.search(query).hits > settings.get('MAX_PER_DOMAIN'):
            # Do not execute this request
            request.meta['proxy'] = ""
            msg = "Ignoring request {}, More than 1000 sites crawled from this domain.".format(request.url)
            log.msg(msg, level=log.INFO)
            raise IgnoreRequest()

class SubDomainLimit(object):
    """
    Ignore weird sub domain loops (for instance, rss.rss...rss.rss.something.onion)
    """
    def process_request(self, request, spider):
        hostname = urlparse(request.url).hostname
        if len(hostname.split(".")) > 4:
            # Do not execute this request
            request.meta['proxy'] = ""
            msg = "Ignoring request {}, too many sub domains.".format(request.url)
            log.msg(msg, level=log.INFO)
            raise IgnoreRequest()

class IgnoreAlreadyCrawledUrlsMiddleware(object):
    """
    Middleware to check is this URL crawled lately and
    ignores those URLs that have been crawled.
    """
    def process_request(self, request, spider):
        url = request.url
        id_str = 'ahmia.websiteindex.' + hashlib.sha256(url).hexdigest()
        solr = pysolr.Solr(settings.get('SOLR_CONNECTION'), timeout=10)
        results = solr.search("id:"+id_str)
        time_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        # If there are duplicate IDs in the Solr database
        if len(results) > 1:
            # This should never happend
            raise Exception("Error in the Solr database! Duplicate IDs!")
        for result in results:
            created = result['date_inserted']
            created = datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
            time_now = datetime.datetime.strptime(time_now, '%Y-%m-%dT%H:%M:%SZ')
            delta = time_now - created
            if delta.days < settings.get('FRESH_INTERVAL'):
                # Do not execute this request
                request.meta['proxy'] = ""
                msg = "Ignoring request {}, URL has been crawled.".format(request.url)
                log.msg(msg, level=log.INFO)
                raise IgnoreRequest()

class ProxyMiddleware(object):
    """Middleware for .onion addresses."""
    def process_request(self, request, spider):
        parsed_uri = urlparse( request.url )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if ".onion" in domain and not ".onion." in domain:
            request.meta['proxy'] = settings.get('HTTP_PROXY')



# Middleware to exclude any response type that isn't in a whitelist


class FilterResponses(object):
    """Limit the HTTP response types that Scrapy downloads."""

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
