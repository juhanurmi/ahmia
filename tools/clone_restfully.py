# -*- coding: utf-8 -*-

from urllib2 import Request
import urllib2
import simplejson


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
    	from_url = 'https://ahmia.fi/address/'
	where_url = 'http://127.0.0.1:8000/address/'
	answer_txt = getjson( from_url )
	clone( answer_txt, where_url )


def clone( txt, url ):
	json = simplejson.loads( txt )
	for hs in json['onions']:
		post( url, simplejson.dumps(hs) )


def getjson( url ):
	txt = ""
	try:
		req = urllib2.Request( url, headers={'Content-type': 'application/json'} )
        	txt = urllib2.urlopen(req).read()
		return txt
        except urllib2.HTTPError, e:
                return txt 



if __name__ == '__main__':
	get_old_page_data()


