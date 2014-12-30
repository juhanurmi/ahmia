"""Gather backlinking information."""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files
import datetime  # Timestamp to each JSON file
import json  # JSON library
import os  # Reading directories
import random  # For random sleep time
import subprocess  # To call command line
import time  # For sleep()

import urllib3  # To HTTP requests

import module_locator  # My module.locator.py


def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()

def valid_pretty_json(myjson):
    """Check that text string is valid JSON and return pretty print."""
    try:
        parsed = json.loads(myjson)
        pretty = json.dumps(parsed, indent=4, sort_keys=True,
        ensure_ascii=False)
        return pretty
    except ValueError:
        return False

def get_backlinks(onion_url):
    """ Call backlink tester and return the number of backlinks. """
    my_path = module_locator.module_path()
    backlink_tool = my_path + "/backlinkers.py"
    args = ["python", backlink_tool, "-c", onion_url]  # TODO: use the new backlinker spider instead?
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    count = int(proc.communicate()[0])
    return count

def save_popularity_data(data, onion_id):
    """ Save the popularity data to """
    my_path = module_locator.module_path()
    document_dir = my_path.replace("/tools", "/popularity_stats/")
    document_dir = document_dir + datetime.datetime.now().strftime("%y-%m-%d")
    if not os.path.exists(document_dir):
        os.makedirs(document_dir)
    pretty_data = valid_pretty_json(data)
    text2file(pretty_data, document_dir + "/" + onion_id + ".json")

def main():
    """Main function."""
    # Gather all backlink information from the rest
    timestamp = datetime.datetime.now().strftime("%y-%m-%d")
    stats_dir = "/popularity_stats/" + timestamp + "/"
    url = 'https://127.0.0.1:45454/address/online/'
    pool = urllib3.HTTPSConnectionPool("127.0.0.1", 45454, timeout=10,
    cert_reqs='CERT_NONE', assert_hostname=False)
    links = pool.request('GET', url).data
    links = links.replace(".onion/", "").replace("http://", "").split('\n')
    for onion_id in links:
        try:
            # Random delay 3min + 1-60 seconds
            delay_time = 180 + random.randrange(1, 60)
            time.sleep(delay_time)
            if not onion_id:
                continue
            content_type = {'Content-Type':'application/json'}
            onion_url = 'http://' + onion_id + '.onion/'
            print onion_url
            backlinks = str(get_backlinks(onion_url))
            url = 'https://127.0.0.1:45454/address/' + onion_id + "/popularity/"
            data = '{"date": "' + timestamp + '", "tor2web_access_count": '
            data = data + '0, "backlinks": ' + backlinks + '}'
            print data
            save_popularity_data(data, onion_id)
            pool.urlopen('PUT', url, headers=content_type, body=data)
        except Exception:
            import traceback
            print 'generic exception: ' + traceback.format_exc()

if __name__ == '__main__':
    main()
