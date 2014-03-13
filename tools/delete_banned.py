# -*- coding: utf-8 -*-

from urllib2 import Request
import urllib2
import base64


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
        if not open(req):
		print url


def delete_hidden_services():
    	urldomains = 'https://127.0.0.1/banneddomains.txt'
	links = get2txt( urldomains ).split('\n')
    	for link in links:
		if not link:
			continue
		print link
		id = link[7:-7]
		url = 'http://10.8.0.6/solr/collection1/update?stream.body=<delete><query>host_s:'+id+'.onion</query></delete>&commit=true'
		send_get(url)
		


def get2txt( url ):
        txt = ""
        try:
                txt = urllib2.urlopen( url ).read()
                return txt
        except urllib2.HTTPError, e:
                return txt


if __name__ == '__main__':
	delete_hidden_services()

