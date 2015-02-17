"""
Read JSON files from ./history
and split them to multiple files under ./history_multiple.
"""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files
import json  # JSON library
import os  # Reading directories

import module_locator  # My module.locator.py


def cut_drugs(drugs, collection):
    """Splits the JSON to multiple files."""
    print "Instances in drug collection: %d" % collection.count()
    print "Adding company data to trunk collection..."
    for category_obj in drugs["Nautintoaineet"]:
        for category in category_obj:
            for subcategory_obj in category_obj[category]:
                for subcategory in subcategory_obj:
                    for product_obj in subcategory_obj[subcategory]:
                        product_obj["year"] = drugs["year"]
                        product_obj["month"] = drugs["month"]
                        product_obj["day"] = drugs["day"]
                        product_obj["subcategory"] = subcategory
                        product_obj["category"] = category
                        collection.insert(product_obj)
    print "Instances in drug collection: %d" % collection.count()
    print "Done."

def getKey(item):
    """Return key."""
    return item.keys()[0]

def main():
    """Main function."""
    my_path = module_locator.module_path()
    json_data_dir = my_path.replace("/tools", "/tor2web_stats/")
    onions_data = {}
    onions = []
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
                    onions.append(onion)
    static_log = my_path.replace("/tools", "/ahmia/static/log/onion_site_history/")
    for onion in onions_data.keys():
        data = onions_data[onion]
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
