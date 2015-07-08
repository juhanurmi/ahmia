"""Data analyser for the access.log."""
# -*- coding: utf-8 -*-
import codecs  # UTF-8 support for the text files
import datetime  # To compare Apache log timestamps
import json  # JSON library
import os
import re  # Regular expressions
import time  # To compare Apache log timestamps

import module_locator  # My module.locator.py


def valid_pretty_json(myjson):
    """Check that text string is valid JSON."""
    try:
        parsed = json.loads(myjson)
        pretty = json.dumps(parsed, indent=4, sort_keys=True,
        ensure_ascii=False)
        return pretty
    except ValueError:
        return False

def text2file(txt, filename):
    """Write the txt to the file."""
    outputfile = codecs.open(filename, "w", "utf-8")
    outputfile.write(txt)
    outputfile.close()

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

def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        total_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(total_size, offset + buf_size)
            fh.seek(-offset, os.SEEK_END)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                yield lines[index]
        yield segment

def analyser(access_file_path):
    """Extracts information from the access log text."""
    regex1 = r'([(\d\.)]+) - - \[(.*?)\] "(.*?)"'
    #regex2 = re.compile(r'\/search\/\?q=(.*?) HTTP')
    search_counts = []
    search_count = 0
    timestamp1 = ""
    for line in reverse_readline(access_file_path):
        if line:
            try:
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
            except Exception as e:
                print e
    json_data = '{"searches": [' + ",".join(search_counts) + ']}'
    json_pretty = valid_pretty_json(json_data)
    if json_pretty:
        return json_pretty

def main():
    """Main function."""
    my_path = module_locator.module_path()
    access_file_path = my_path.replace("/tools", "/error/access.log")
    json_pretty = analyser(access_file_path)
    filename = my_path.replace("/tools", "/ahmia/static/log/access.json")
    text2file(json_pretty, filename)
    access_file_path = my_path.replace("/tools", "/error/hs_access.log")
    json_pretty = analyser(access_file_path)
    filename = my_path.replace("/tools", "/ahmia/static/log/hs_access.json")
    text2file(json_pretty, filename)

if __name__ == '__main__':
    main()
