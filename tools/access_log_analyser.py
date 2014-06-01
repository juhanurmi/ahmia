"""Data analyser for the access.log."""
# -*- coding: utf-8 -*-
import codecs # UTF-8 support for the text files
import re # Regular expressions
import module_locator # My module.locator.py
import time # To compare Apache log timestamps
import datetime # To compare Apache log timestamps
import json # JSON library

def valid_pretty_json(myjson):
    """Check that text string is valid JSON."""
    try:
        parsed = json.loads(myjson)
        pretty = json.dumps(parsed, indent=4, sort_keys=True,
        ensure_ascii=False)
        return pretty
    except ValueError:
        return False

def date_compare(ts1, ts2, **compkw):
    """
        Compares to Apache log format dates.
        Return true if distance between dates is greater than
        **compkw = ['days', 'hours', 'minutes', 'seconds'].
    """
    time1 = time.strptime(ts1.strip('[]').split()[0], '%d/%b/%Y:%H:%M:%S')
    date1 = datetime.datetime(*time1[:6])
    time2 = time.strptime(ts2.strip('[]').split()[0], '%d/%b/%Y:%H:%M:%S')
    date2 = datetime.datetime(*time2[:6])
    delta = abs(date2-date1)
    #order_list = ['days', 'hours', 'minutes', 'seconds']
    #out_list = []
    #for item in order_list:
        #if compkw.has_key(item):
            #out_list.append('%s %s' % (compkw[item], item))
    #out_str = ', '.join(out_list)
    if delta <= datetime.timedelta(**compkw):
        #print 'Less than or equal to %s' % (out_str)
        return False
    #print 'Greater than %s' % (out_str)
    return True

def search_term_unescape(text):
    """Produces readable query text."""
    escape_table = {
    "%20": " ",
    "+": " ",
    "%21": "!",
    "%22": '"',
    "%23": "#",
    "%24": "$",
    "%25": "%",
    "%26": "&",
    "%27": "'",
    "%28": "(",
    "%29": ")",
    "%2a": "*",
    "%2b": " ",
    "%2B": " ",
    "%2c": ",",
    "%2C": ",",
    "%2d": "-",
    "%2D": "-",
    "%2e": ".",
    "%2f": "/",
    "%2F": "/",
    "%3a": ":",
    "%3A": ":",
    "%3b": ";",
    "%3c": "<",
    "%3d": "=",
    "%3e": ">",
    "%3f": "?",
    "%40": "@",
    "%5b": "[",
    "%5c": "\\",
    "%5d": "]",
    "%7b": "{",
    "%7c": "|",
    "%7d": "}",
    "%7e": "~"
    }
    return "".join(escape_table.get(c, c) for c in text)

def read_file(filename):
    """Read a file and return the text content."""
    inputfile = codecs.open(filename, "r", "utf-8")
    data = inputfile.read()
    inputfile.close()
    return data

def analyser(access_log):
    """Extracts information from the access log text."""
    regex1 = r'([(\d\.)]+) - - \[(.*?)\] "(.*?)"'
    #regex2 = re.compile(r'\/search\/\?q=(.*?) HTTP')
    search_counts = []
    search_count = 0
    timestamp1 = ""
    for line in reversed(access_log.split('\n')):
        if line:
            ip_addr, timestamp2, http = re.match(regex1, line).groups()
            if not timestamp1:
                timestamp1 = timestamp2
            if date_compare(timestamp1, timestamp2, hours=1):
                searches = '{"' + timestamp1 + '": ' + str(search_count) + '}'
                search_counts.append(searches)
                search_count = 0
                timestamp1 = timestamp2
            if "/search/?q=" in http:
                search_count = search_count + 1
                #query = regex2.search(http)
                #if query:
                    #query = search_term_unescape(query.group(1))
                    #if not "%" in query:
                        #print query
    json_data = '{"searches": [' + ",".join(search_counts) + ']}'
    json_pretty = valid_pretty_json(json_data)
    if json_pretty:
        print json_pretty

def main():
    """Main function."""
    my_path = module_locator.module_path()
    access_file_path = my_path.replace("/tools", "/error/access.log")
    access_log = read_file(access_file_path)
    analyser(access_log)

if __name__ == '__main__':
    main()
