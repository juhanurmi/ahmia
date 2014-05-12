# -*- coding: utf-8 -*-

from urllib2 import Request
import urllib2
import base64
from xml.dom.minidom import parse, parseString
import cgi
import re


def open(req):
	try:
		handle = urllib2.urlopen(req)
		if handle.getcode() != 200:
			print handle.getcode()
		else:
			return True
	except urllib2.HTTPError, e:
		print('HTTPError = ' + str(e.code))
	except urllib2.URLError, e:
		print('URLError = ' + str(e.reason))
	except Exception:
		import traceback
		print('generic exception: ' + traceback.format_exc())
	return False


def post(url,data):
        req = Request(url)
        req.add_data(data)
        req.get_method = lambda: 'POST'
        if not open(req):
		print url
		print data


def get_old_page_data():
	urlpost = 'http://ahmia.fi:40404/address/'
    	urldomains = 'https://ahmia.fi/oniondomains.txt'
	links = get2txt( urldomains ).split('\n')
    	for link in links:
		if not link:
			continue
		print link
		id = link[7:-7]
		urlrdf = 'https://ahmia.fi/rdf/'+id+'.rdf'
		rdfcontent = get2txt(urlrdf)
		if rdfcontent:
			data = rdf2data( rdfcontent, link )
		else:
			data = '{"url":"' + link  + '"}'
		post(urlpost,data)


def rdf2data( rdfcontent, link ):
	dom = parseString( rdfcontent )
	dc_namespace = "http://purl.org/dc/elements/1.1/"

        title_node = dom.getElementsByTagNameNS( dc_namespace, "title" )[0].firstChild
        if title_node:
                title = cgi.escape(title_node.nodeValue).replace('"', "'")
	else:
		title = ""

        description_node = dom.getElementsByTagNameNS( dc_namespace, "description" )[0].firstChild
        if description_node:
                description = cgi.escape(description_node.nodeValue).replace('"', "'")
	else:
		description = ""

        relation_node = dom.getElementsByTagNameNS( dc_namespace, "relation" )[0].firstChild
        if relation_node:
                relation = cgi.escape(relation_node.nodeValue).replace('"', "'")
	else:
		relation = ""

        subject_node = dom.getElementsByTagNameNS( dc_namespace, "subject" )[0].firstChild
        if subject_node:
                subject = cgi.escape(subject_node.nodeValue).replace('"', "'")
	else:
		subject = ""

	type_node = dom.getElementsByTagNameNS( dc_namespace, "type" )[0].firstChild
	if type_node:
		type = cgi.escape(type_node.nodeValue).replace('"', "'")  
	else:
		type = ""

	data = '{"url":"' + link  + '","title":"' + title + '","description":"' + description  + '","relation":"' + relation + '","subject":"' + subject + '","type":"' + type + '"}'

	asciidata = data.encode("ascii","ignore")
	asciistripped = asciidata.rstrip()
	data = re.sub( ' +',' ', asciistripped )
	data = data.replace("\n", " ")
	#data = unicode( data, "utf-8" )
	#data = data.decode('utf8')
	return data

def get2txt( url ):
	txt = ""
	try:
        	txt = urllib2.urlopen( url ).read()
		return txt
        except urllib2.HTTPError, e:
                return txt 



if __name__ == '__main__':
	get_old_page_data()

