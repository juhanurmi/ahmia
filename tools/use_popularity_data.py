"""Use the data from Tor2web nodes."""
# -*- coding: utf-8 -*-
import urllib3 #To HTTP requests
import codecs # UTF-8 support for the text files
import json # JSON library
import datetime # Timestamp to each JSON file
import os # Reading directories
import module_locator # My module.locator.py
import subprocess #To call command line

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
    args = ["python", backlink_tool, "-c", onion_url]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    count = int(proc.communicate()[0])
    return count

def analyser(json_file, checked_onions):
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
            if onion_id in checked_onions:
                continue
            onion_url = 'http://' + onion_id + '.onion/'
            print onion_url
            data = '{"url": "' + onion_url + '"}'
            url = 'https://127.0.0.1/address/'
            content_type = {'Content-Type':'application/json'}
            pool.urlopen('POST', url, headers=content_type, body=data)
            backlinks = str(get_backlinks(onion_url))
            url = url + onion_id + "/popularity/"
            data = '{"date": "' + dateday + '", "tor2web_access_count": '
            data = data + str(access_count) + ',"backlinks":' + backlinks + '}'
            print data
            save_popularity_data(data, onion_id)
            pool.urlopen('PUT', url, headers=content_type, body=data)
            checked_onions.append(onion_id)

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
    my_path = module_locator.module_path()
    document_dir = my_path.replace("/tools", "/tor2web_stats/")
    timestamp = datetime.datetime.now().strftime("%y-%m-%d")
    timestamp = "_" + timestamp + "-"
    checked_onions = []
    # Use Tor2web stats
    for filename in os.listdir(document_dir):
        if not filename.endswith(".json"):
            continue
        if timestamp in filename:
            analyser(document_dir+filename, checked_onions)
    # Gather all backlink information from the rest
    timestamp = datetime.datetime.now().strftime("%y-%m-%d")
    stats_dir = "/popularity_stats/" + timestamp + "/"
    document_dir = document_dir.replace("/tor2web_stats/", stats_dir)
    url = 'https://127.0.0.1/address/online/'
    pool = urllib3.HTTPSConnectionPool("127.0.0.1", 443, timeout=10,
    cert_reqs='CERT_NONE', assert_hostname=False)
    links = pool.request('GET', url).data
    links = links.replace(".onion/", "").replace("http://", "").split('\n')
    for onion_id in links:
        if not onion_id or onion_id in checked_onions:
            continue
        content_type = {'Content-Type':'application/json'}
        onion_url = 'http://' + onion_id + '.onion/'
        print onion_url
        backlinks = str(get_backlinks(onion_url))
        url = 'https://127.0.0.1/address/' + onion_id + "/popularity/"
        data = '{"date": "' + timestamp + '", "tor2web_access_count": '
        data = data + '0, "backlinks": ' + backlinks + '}'
        print data
        save_popularity_data(data, onion_id)
        pool.urlopen('PUT', url, headers=content_type, body=data)

if __name__ == '__main__':
    main()
