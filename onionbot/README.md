dirbot
======

This is a Scrapy project to crawl .onion websites from the Tor network.

It requires Tor software (use Tor2web mode), Privoxy, and the data is saved to Apache Solr.

Short guide to Onionbot
-----------------------

- Install Tor in Tor2web mode
- Install Polipo
- Install Solr

Make sure your Solr is empty (delete all):

```sh
http://localhost:8080/solr/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E&commit=true
```

Configurate the schema to Solr:

```sh
$ cp /etc/solr/conf/schema.xml schema.xml.backup
$ sudo cp ahmia/solr/schema.xml /etc/solr/conf/schema.xml
$ sudo cp ahmia/solr/stopwords_en.txt /etc/solr/conf/
$ sudo service tomcat6 restart
```

Setup Polipo:

```sh
$ cp ahmia/polipo_conf /etc/polipo/config
$ service polipo restart
```

Edit the crawler's DEPTH_LIMIT = 1:

```sh
$ nano ahmia/onionbot/dirbot/settings.py
```

Run the crawler software:

```sh
$ scrapy crawl OnionSpider -o items.json -t json
```

Inject the JSON data to Solr:

```sh
$ python inject.py items.json http://127.0.0.1:8080/solr/
```

Test your Sorl:

```sh
http://127.0.0.1:8080/solr/select/?q=*%3A*&version=2.2&start=0&rows=10&indent=on
```

Items
-----

The items scraped by this project are websites, and the item is defined in the

```
dirbot.items.CrawledWebsiteItem
```

and the data is

```
domain, url, tor2web_url, title, text, date_inserted
```

Spiders
-------

This project contains one spider called `OnionSpider` that you can see by running:

```sh
$ scrapy list
Spider: OnionSpider
```

Middlewares
-----------

Middlewares define HTTP proxy for .onion domains. Note that only .onion domains can be crawled using the HTTP proxy.

Furthermore, non-text responses are filtered out.
