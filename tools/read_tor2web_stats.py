"""
Read JSON files from ./history
and split them to multiple files under ./history_multiple.
"""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files
import json  # JSON library
import os  # Reading directories

import requests

import module_locator  # My module.locator.py


def getKey(item):
    """Return key."""
    return item.keys()[0]

def main():
    """Main function."""
    my_path = module_locator.module_path()
    json_data_dir = my_path.replace("/tools", "/tor2web_stats/")
    onions_data = {}
    for filename in os.listdir(json_data_dir):
        if filename.endswith(".json"):
            json_file = json_data_dir + filename
            json_data = open(json_file)
            day_data = json.load(json_data)
            json_data.close()
            time_stamp = day_data["date"].encode("ascii", "ignore")
            for onion_data in day_data["hidden_services"]:
                onion = onion_data["id"].lower()
                access_count = int(onion_data["access_count"])
                try:
                    found = False
                    last_time_stamp = onions_data[onion]#[-1].keys()[0]
                    for o in onions_data[onion]:
                        if o.keys()[0] == time_stamp:
                            o[time_stamp] = o[time_stamp] + access_count
                            found = True
                            break
                    if not found:
                        onions_data[onion].append({time_stamp: access_count})
                except:
                    onions_data[onion] = []
                    onions_data[onion].append({time_stamp: access_count})
    static_log = my_path.replace("/tools", "/ahmia/static/log/onion_site_history/")
    onions = []

    # Filter banned domains, get the list first
    r = requests.get('https://127.0.0.1/banneddomains.txt', verify=False)
    text = r.text.encode('ascii')
    text = text.replace("http://", "")
    text = text.replace("https://", "")
    text = text.replace(".onion/", "")
    ban_list = text.split("\n")

    # Print to files
    for onion in onions_data.keys():
        data = onions_data[onion]
        # Only show those onions that have over 100 active days
        # Filter out banned domains
        if len(data) > 100 and not onion in ban_list:
            onions.append(onion)
        if not onion in ban_list:
            data = sorted(data, key=getKey)
            pretty = json.dumps(data, indent=4, ensure_ascii=False)
            file = open(static_log + onion + ".json", "w")
            file.write(pretty+"\n")
            file.close()
    onions.sort()
    pretty = json.dumps(onions, indent=4, sort_keys=True, ensure_ascii=False)
    file = open(static_log + "onions.json", "w")
    file.write(pretty+"\n")
    file.close()

if __name__ == '__main__':
    main()
