# -*- coding: utf-8 -*-
# test all hidden service's: HTTP GET tells if the service is online

from urllib2 import Request
import urllib2
import socket
socket.setdefaulttimeout(60)


def open(req):
	try:
		handle = urllib2.urlopen(req)
		if handle.getcode() != 200:
			print handle.getcode()
		else:
			print handle.read()
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


def test_hidden_services():
    	urldomains = 'https://127.0.0.1/alldomains'
	links = get2txt( urldomains ).split('\n')
    	for link in links:
		if not link:
			continue
		print link
		urlpost = 'https://ahmia.fi/address/'
		id = link[7:-7]
		urlpost = urlpost + id + "/status"
		data = ""
		post(urlpost,data)
		


def get2txt( url ):
        txt = ""
        try:
                txt = urllib2.urlopen( url ).read()
                return txt
        except urllib2.HTTPError, e:
                return txt


if __name__ == '__main__':
	test_hidden_services()

