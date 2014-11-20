"""This program tests the popularity of the target sites.
Give list of target sites and host of the backlinker."""

import argparse  # To command line arguments

import certifi  # Security: Verified HTTPS with SSL/TLS
import urllib3  # To HTTP requests
from bs4 import BeautifulSoup  # To parse HTML


def load_content(site, host, links):
    """Tests a site."""
    # Security: Verified HTTPS with SSL/TLS
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )
    start_page_search = """https://startpage.com/do/search
    ?cmd=process_search&language=english&enginecount=1&pl=&abp=
    1&cdm=&tss=1&ff=&theme=&prf=464341bcfbcf47b736ff43307aef287a
    &suggestOn=1&flag_ac=0&lui=english&cat=web&query="""
    start_page_search = start_page_search.replace('\n', '')
    start_page_search = start_page_search.replace(' ', '')
    if host:
        start_page_search = start_page_search + "host%3A"+host+"+"
    start_page_search = start_page_search+"link%3A"+site
    if not links:
        start_page_search = start_page_search.replace("link%3A", "")
    response = http.request('GET', start_page_search)
    return response

def find_between(string, first, last):
    """Return substring between 'first' and 'last'."""
    try:
        start = string.index(first) + len(first)
        end = string.index(last, start)
        return string[start:end]
    except ValueError:
        return ""

def backlinks(response, count):
    """Print all backlinkers."""
    if response.status == 200:
        html_content = response.data
        soup = BeautifulSoup(html_content, "html5lib")
        if count:
            result_count(soup)
        else:
            number_of_results(soup)
            results(soup)
    else:
        print "HTTP status: %d" % response.status

def result_count(soup):
    """Print only the number of backlinkers."""
    element = soup.find("p", {"id": "results_count_p"})
    if element:
        number = find_between(element.contents[0], "About ", " results")
        number = number.replace(",", "")
        print int(number)
    else:
        print 0

def number_of_results(soup):
    """Print the number of backlinkers."""
    print "------------------------"
    element = soup.find("p", {"id": "results_count_p"})
    if element:
        print element.contents[0]
        print "Some entries are omitted: the most relevant results are shown."
    else:
        print "0 results"
    print "------------------------"

def results(soup):
    """Print each backlinker."""
    h3_elements = soup.find_all('h3')
    for h3_element in h3_elements:
        for link in h3_element.find_all('a'):
            url = link.get('href')
            if not "http://www.google.com/" in url:
                print url

def crawler(url, host, links, count):
    """Crawler is searching backlinks from the given host."""
    resp = load_content(url, host, links)
    backlinks(resp, count)

def get_command_args(parser):
    """Reads command line arguments."""
    parser.add_argument('-b', '--backlinker', required=False)
    parser.add_argument('-l', '--links', action='store_true', required=False)
    parser.add_argument('-c', '--count', action='store_true', required=False)
    parser.add_argument('target', nargs='*')
    args = parser.parse_args()
    links = args.links
    count = args.count
    targetsite = args.target
    host = args.backlinker
    if targetsite:
        targetsite = ''.join(targetsite[0].split())
        if not count:
            print "Searching backlinks to %s" % targetsite
    else:
        print "You need to give one target site."
        raise SystemExit
    if host:
        host = ''.join(host.split())
        if not count:
            print "Checking backlinks from the host %s" % host
    else:
        if not count:
            print "Checking backlinks from the host ANY"
    return targetsite, host, links, count

def main():
    """Main function."""
    desc = "Search backlinks to the target site."
    parser = argparse.ArgumentParser(description=desc)
    targetsite, host, links, count = get_command_args(parser)
    crawler(targetsite, host, links, count)

if __name__ == '__main__':
    main()
