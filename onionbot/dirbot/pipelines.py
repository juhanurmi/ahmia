import datetime
import hashlib
from urlparse import urlparse

import pysolr


class SolrPipeline(object):
    """A pipeline for saving the crawled data to Apache Solr"""

    def process_item(self, item, spider):
        index = hashlib.sha256(item['url']).hexdigest()
        item['id'] = 'ahmia.websiteindex.' + str(index)
        item['django_ct'] = 'ahmia.websiteindex'
        item['django_id'] = index
        parsed_uri = urlparse( item['url'] )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        item['domain'] = domain
        tor2web = domain.replace(".onion", ".tor2web.fi")
        item['tor2web_url'] = item['url'].replace(domain, tor2web)
        time_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        item['date_inserted'] = time_now
        #Delete the old information
        solr = pysolr.Solr("http://127.0.0.1:8080/solr/", timeout=10)
        solr.delete(id=item['id'])
        solr.add([item])
        return item
