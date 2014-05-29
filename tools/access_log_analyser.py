"""Data analyser for the access.log."""
# -*- coding: utf-8 -*-
import codecs # UTF-8 support for the text files
import re # Regular expressions
import module_locator # My module.locator.py

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
    regex2 = re.compile('\/search\/\?q=(.*?) HTTP')
    search_count = 0
    for line in access_log.split('\n'):
        if line:
            ip_addr, timestamp, http = re.match(regex1, line).groups()
            if "/search/?q=" in http:
                search_count = search_count + 1
                query = regex2.search(http)
                if query:
                    query = search_term_unescape(query.group(1))
                    if not "%" in query:
                        print query
    print search_count

def main():
    """Main function."""
    my_path = module_locator.module_path()
    access_file_path = my_path.replace("/tools", "/error/access.log")
    access_log = read_file(access_file_path)
    analyser(access_log)

if __name__ == '__main__':
    main()
