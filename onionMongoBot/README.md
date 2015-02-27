onionMongoBot - Crawl .onion websites from the Tor network
==========================================================

This is a Scrapy project to crawl .onion websites from the Tor network. Saves h1, h2, title, domain, url, plain HTML and words to MongoDB or plain JSON.

Short guide to the crawler installation
---------------------------------------

- Install MongoDB
- Install Python 2.7
- Install Tor software (use Tor2web mode patch)
- Install Polipo HTTP proxy software

```sh
$ sudo apt-get install python-pip
$ sudo apt-get install libffi-dev
$ sudo apt-get install python-dev libxml2-dev libxslt-dev
$ sudo apt-get install html2text
$ sudo apt-get install python-html2text
$ sudo apt-get install python-twisted
$ sudo apt-get install python-pyopenssl
$ sudo apt-get install python-simplejson
$ pip install cryptography
$ pip install scrapy
$ pip install scrapy-mongodb
```

Setup Polipo:

```sh
$ cp ahmia/polipo_conf /etc/polipo/config
$ service polipo restart
```

Run the crawler software:

```sh
$ scrapy crawl OnionSpider -s DEPTH_LIMIT=3
or
$ scrapy crawl OnionSpider -o items.json -t json
```

MongoDB objects are like:

```json
{
        "_id" : ObjectId("54eea240cd9aa9f4f6646be9"),
        "h2" : "",
        "domain" : "23bteufi2kcqza2l.onion",
        "html" : "<html><body bgcolor=#424242><p style='font-family:Tahoma;font-size:24px;color:#FF0000'><br><b>Enter your key:<b><br></p><p style='font-family:Tahoma;font-size:16px;color:#FFFFFF'>Enter your public key and press 'Send'<br><form method='POST' action='/keyrecovery'><textarea autofocus name='key' placeholder='Enter you public key here' rows=4 cols=80 style='font-family:Courier New;font-size:16px'></textarea><br><br><input type='submit' value='Send' style='font-family:Tahoma;font-size:16px'></form></p></body></html>",
        "words" : " Enter your key: Enter your public key and press 'Send'",
        "title" : "",
        "url" : "http://23bteufi2kcqza2l.onion/",
        "h1" : "",
        "scrapy-mongodb" : {
                "ts" : ISODate("2015-02-26T04:34:08.334Z")
        }
}
```
