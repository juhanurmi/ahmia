# -*- coding: utf-8 -*-

from urllib2 import Request
import urllib2
import base64
import xml.etree.ElementTree as ET #XML
import re

#test is url correct onion url
#Must be like http://3g2upl4pq6kufc4m.onion/
def validate_onion_URL( url ):
    if len(url) != 30:
        return False
    if url[0:7] != 'http://':
        return False
    if url[-7:] != '.onion/':
        return False
    if not re.match( "[a-z2-7]{16}", url[7:-7] ):
        return False
    return True


def open(req):
	try:
		handle = urllib2.urlopen(req)
		if handle.getcode() != 200:
			print handle.getcode()
		else:
			return handle.read()
	except urllib2.HTTPError, e:
		print('HTTPError = ' + str(e.code))
	except urllib2.URLError, e:
		print('URLError = ' + str(e.reason))
	except Exception:
		import traceback
		print('generic exception: ' + traceback.format_exc())
	return False

#BASE64_CREDENTIALS=$(echo -n "<username>:<password>" | base64)
#curl -i --header "Authorization:Basic ${BASE64_CREDENTIALS}" <url>
def auth(req):
        username = 'solr-access'
        password = 'E51Zs9l9Gfd7kzN67v9OldTEVw'
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        header = "Basic %s" % base64string
        req.add_header("Authorization", header)


def send_get(url):
        req = Request(url)
        auth(req)
	result = open(req)
        if not result:
		print "Error..."
		return ""

	return result


def add_hidden_services(start):
	found = False
	start_str = '%d' % start
	#urldomains = 'http://10.8.0.6/solr/select?q=host_s:*&defType=edismax&start=0&core=collection1&fl=host_s&facet=on&facet.field=host_s&rows=9999'
	urldomains = 'http://10.8.0.6/solr/select?q=host_s:*&defType=edismax&start='+start_str+'&core=collection1&fl=host_s&rows=10100'
	XML_string = send_get( urldomains )
	try:
		root = ET.fromstring(XML_string) #<response>
		result = root.find('result') #<result>
		for doc in result.findall('doc'):
			for str in doc.findall('str'):
				if "host_s" in str.get('name'):
					domain = "http://"+str.text+"/"
					if validate_onion_URL(domain):		
						print('{"url":"'+domain+'"}')		
						found = True
	except:
		print XML_string		

	return found


if __name__ == '__main__':
	start = 0
	while True:
		if not add_hidden_services(start):
			break
		start = start + 10000
