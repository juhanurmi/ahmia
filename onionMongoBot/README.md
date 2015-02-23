onionMongoBot - Crawl .onion websites from the Tor network
==========================================================

This is a Scrapy project to crawl .onion websites from the Tor network. Saves plain HTML text to MongoDB or plain JSON.

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
        "_id" : ObjectId("54eb6ccf16ed1b2b079acb5a"),
        "h2" : "",
        "domain" : "23swqgocas65z7xz.onion",
        "html" : "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\"/>\n<style type=\"text/css\">\n\nbody {\n\tbackground-image: url(logo.png);\n\tbackground-repeat: no-repeat no-repeat;\n\tbackground-position: center center;\n\t-webkit-background-size: cover;\n   \t-moz-background-size: cover;\n   \t-o-background-size: cover;\n   \tbackground-attachment: fixed;\n}\n\n</style>\n<title>Alert!</title>\n</head>\n\n<body>\t\n</body>\n\n</html>\n\n",
        "scrapy-mongodb" : {
                "ts" : ISODate("2015-02-23T18:09:19.211Z")
        },
        "title" : "Alert!",
        "url" : "http://23swqgocas65z7xz.onion/",
        "h1" : ""
}
```
