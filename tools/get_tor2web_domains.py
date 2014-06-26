"""Load each tor2web node's visited domain list."""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files
import datetime  # Timestamp to each JSON file
import json  # JSON library

import urllib3  # To HTTP requests


def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()

def valid_pretty_json(myjson):
    """Check that text string is valid JSON."""
    try:
        parsed = json.loads(myjson)
        pretty = json.dumps(parsed, indent=4, sort_keys=True,
        ensure_ascii=False)
        return pretty
    except ValueError:
        return False

def loader(tor2web_nodes):
    """Load visited domains information from tor2web nodes."""
    for node in tor2web_nodes:
        print "\n Trying download from the %s \n" % node
        json_data = get_json("abcd." + node)
        if not json_data:
            continue
        pretty_json = valid_pretty_json(json_data)
        if pretty_json:
            timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
            node = node.replace(".", "") + "_"
            filename = "/usr/local/lib/ahmia/tor2web_stats/" + node + timestamp + ".json"
            text2file(pretty_json, filename)
            print "Downloaded JSON data."

def get_json(node):
    """Send HTTP GET request to download JSON list."""
    try:
        http = urllib3.HTTPSConnectionPool(node, 443, timeout=10,
        cert_reqs='CERT_NONE', assert_hostname=False)
        response = http.request('GET', "/antanistaticmap/stats/yesterday")
    except Exception as error:
        print error
        return ""
    if response.status == 200:
        return response.data
    else:
        return ""

def main():
    """Main function."""
    tor2web_nodes = ["tor2web.fi", "tor2web.org", "onion.to",
    "tor2web.blutmagie.de", "onion.lt", "onion.cab", "onion.lu"]
    loader(tor2web_nodes)

if __name__ == '__main__':
    main()
