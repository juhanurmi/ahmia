import argparse
import json

import pysolr

parser = argparse.ArgumentParser(description='load json into python.')
parser.add_argument('input_file', metavar='input', type=str, help='json input file')
parser.add_argument('solr_url', metavar='url', type=str, help='solr URL')

args = parser.parse_args()
solr = pysolr.Solr(args.solr_url, timeout=10)

items = json.load(open(args.input_file))

solr.add(items)
