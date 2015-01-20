OnionBot
========

This is a Scrapy project to crawl .onion websites from the Tor network.

It requires Tor software (use Tor2web mode), Polipo, and the data is saved to Apache Solr.

Short guide to OnionBot
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

Run the crawler software and produce JSON file:

```sh
$ scrapy crawl OnionSpider -o items.json -t json
```

or something similar with

```sh
$ scrapy crawl OnionSpider -s MAX_PER_DOMAIN=100 -s DEPTH_LIMIT=4
```

Test your Solr:

```sh
http://127.0.0.1:33433/solr/select/?q=*%3A*&version=2.2&start=0&rows=10&indent=on
```

Delete a domain aaaaaaaaaaaaaaaa:

```sh
curl "http://localhost:33433/solr/update?commit=true" -H "Content-Type: text/xml" --data-binary "<delete><query>domain:*aaaaaaaaaaaaaaaa*</query></delete>"
```

Delete old data, older than 14 days:

```sh
curl "http://localhost:33433/solr/update?commit=true" -H "Content-Type: text/xml" --data-binary "<delete><query>date_inserted:[* TO NOW-14DAYS]</query></delete>"
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
