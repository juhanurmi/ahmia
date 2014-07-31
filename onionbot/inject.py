"""
Inject JSON data to Solr database.

Data schema is:

<doc>
    <str name="django_ct">ahmia.websiteindex</str>
    <str name="django_id">1</str>
    <str name="id">ahmia.websiteindex.1</str>
    <str name="text">Onion2 http://2j3wazyk5u4hnvtk.onion/ Onion2</str>
    <str name="title">Onion2</str>
    <str name="url">http://2j3wazyk5u4hnvtk.onion/</str>
</doc>
"""
import argparse
import datetime  # ############
import hashlib
import json
from urlparse import urlparse

import pysolr

parser = argparse.ArgumentParser(description='load json into python.')
parser.add_argument('input_file', metavar='input', type=str, help='json input file')
parser.add_argument('solr_url', metavar='url', type=str, help='solr URL')

args = parser.parse_args()
solr = pysolr.Solr(args.solr_url, timeout=10)

items = json.load(open(args.input_file))

##############
time_now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

for item in items:
    index = hashlib.sha256(item['url']).hexdigest()
    item['id'] = 'ahmia.websiteindex.' + str(index)
    item['django_ct'] = 'ahmia.websiteindex'
    item['django_id'] = index
    parsed_uri = urlparse( item['url'] )
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    item['domain'] = domain
    tor2web = domain.replace(".onion", ".tor2web.fi")
    item['tor2web_url'] = item['url'].replace(domain, tor2web)
    if not item.get('date_inserted'):
        item['date_inserted'] = time_now ##############
    #Delete the old information
    solr.delete(id=item['id'])
    solr.add([item])
