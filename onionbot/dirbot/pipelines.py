import datetime
import hashlib
from urlparse import urlparse

import pysolr
from scrapy.conf import settings


class SolrPipeline(object):
    """A pipeline for saving the crawled data to Apache Solr"""

    def process_item(self, item, spider):
        index = hashlib.sha256(item['url']).hexdigest()
        item['id'] = 'ahmia.websiteindex.' + str(index)
        item['django_ct'] = 'ahmia.websiteindex'
        item['django_id'] = index
        item['crawling_session'] = settings.get('CRAWLING_SESSION')
        parsed_uri = urlparse( item['url'] )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        item['domain'] = domain
        tor2web = domain.replace(".onion", ".tor2web.org")
        item['tor2web_url'] = item['url'].replace(domain, tor2web)
        time_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        item['date_inserted'] = time_now

        # Do not save the content of the banned sites
        banned_domains = settings.get('BANNED_DOMAINS')
        if hashlib.md5(domain).hexdigest() in banned_domains:
            item['text'] = ""

        #Delete the old information
        solr = pysolr.Solr(settings.get('SOLR_CONNECTION'), timeout=10)
        solr.delete(id=item['id'])
        solr.add([item])
        return item
