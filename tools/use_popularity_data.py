"""Use the data from Tor2web nodes."""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files
import datetime  # Timestamp to each JSON file
import json  # JSON library
import os  # Reading directories

import urllib3  # To HTTP requests

import module_locator  # My module.locator.py


def read_file(filename):
    """Read a file and return the text content."""
    inputfile = codecs.open(filename, "r", "utf-8")
    data = inputfile.read()
    inputfile.close()
    return data

def valid_json(myjson):
    """Check that text string is valid JSON."""
    try:
        parsed = json.loads(myjson)
        return parsed
    except ValueError:
        return False

def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()

def analyser(json_file):
    """Analyse JSON data from Tor2web node."""
    print json_file
    pool = urllib3.HTTPSConnectionPool("127.0.0.1", 443, timeout=10,
    cert_reqs='CERT_NONE', assert_hostname=False)
    json_text = read_file(json_file)
    json_data = valid_json(json_text)
    if not json_data:
        print "Error: %s" % json_text
        raise SystemExit
    dateday = json_data["date"]
    if json_data:
        for hidden_service in json_data["hidden_services"]:
            access_count = hidden_service["access_count"]
            onion_id = hidden_service["id"]
            onion_url = 'http://' + onion_id + '.onion/'
            print onion_url
            data = '{"url": "' + onion_url + '"}'
            url = 'https://127.0.0.1/address/'
            content_type = {'Content-Type':'application/json'}
            pool.urlopen('POST', url, headers=content_type, body=data)
            url = url + onion_id + "/popularity/"
            data = '{"date": "' + dateday + '", "tor2web_access_count": '
            data = data + str(access_count) + '}'
            print data
            pool.urlopen('PUT', url, headers=content_type, body=data)

def main():
    """Main function."""
    my_path = module_locator.module_path()
    document_dir = my_path.replace("/tools", "/tor2web_stats/")
    timestamp = datetime.datetime.now().strftime("%y-%m-%d")
    timestamp = "_" + timestamp + "-"
    # Use Tor2web stats
    for filename in os.listdir(document_dir):
        if not filename.endswith(".json"):
            continue
        if timestamp in filename:
            analyser(document_dir+filename)

if __name__ == '__main__':
    main()
