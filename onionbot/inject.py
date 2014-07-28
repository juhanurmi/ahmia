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
import json

import pysolr

parser = argparse.ArgumentParser(description='load json into python.')
parser.add_argument('input_file', metavar='input', type=str, help='json input file')
parser.add_argument('solr_url', metavar='url', type=str, help='solr URL')

args = parser.parse_args()
solr = pysolr.Solr(args.solr_url, timeout=10)

items = json.load(open(args.input_file))

# Add IDs
index = 1
for item in items:
    item['id'] = 'ahmia.websiteindex.' + str(index)
    item['django_ct'] = 'ahmia.websiteindex'
    item['django_id'] = index
    item['text'] = item['title'] + item['text'] + item['url']
    index = index + 1

solr.add(items)
