"""This program downloads the filtering policies from tor2web nodes."""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files

import urllib3  # To HTTP requests

import module_locator  # My module.locator.py


def get_md5list(node):
    """Send HTTP GET request to download JSON list."""
    try:
        http = urllib3.HTTPSConnectionPool(node, 443, timeout=10,
        cert_reqs='CERT_NONE', assert_hostname=False)
        response = http.request('GET', "/antanistaticmap/lists/blacklist")
    except Exception as error:
        print error
        return ""
    if response.status == 200:
        print "The list downloaded."
        return response.data
    else:
        return ""

def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()

def loader(tor2web_nodes):
    """Load visited domains information from tor2web nodes."""
    my_path = module_locator.module_path()
    filename = my_path.replace("/tools", "/ahmia/static/log/")
    for node in tor2web_nodes:
        print "\n Trying download from the %s \n" % node
        md5list = get_md5list("abcd." + node)
        if md5list:
            filename = filename + node + "_md5filterlist.txt"
            text2file(md5list, filename)

def main():
    """Main function."""
    tor2web_nodes = ["tor2web.fi", "tor2web.org", "onion.to",
    "tor2web.blutmagie.de", "onion.lt", "onion.cab", "onion.lu"]
    loader(tor2web_nodes)

if __name__ == '__main__':
    main()
