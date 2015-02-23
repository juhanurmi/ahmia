onionMongoBot - Crawl .onion websites from the Tor network
==========================================================
This is a Scrapy project to crawl .onion websites from the Tor network.
Saves plain HTML text to MongoDB or plain JSON.

Short guide to linksScraper
---------------------------

- Install MongoDB (optional)
- Install Python 2.7
- Install Tor software (use Tor2web mode)
- Install Polipo

```sh
$ sudo apt-get install libffi-dev

$ cd linksScraper
$ virtualenv venv
$ source venv/bin/activate

$ pip install cryptography
$ pip install scrapy
```

Run the crawler software:

```sh
$ scrapy crawl link_spider
or
$ scrapy crawl OnionSpider -o items.json -t json
```

MongoDB objects are like:

```json
{
    "_id" : ObjectId("547454091fd0434347fb012a"),
    "context_url" : "http://www.booxmedia.com/",
    "link_name" : "",
    "link" : "https://twitter.com/booxmedia",
    "scrapy-mongodb" : {
        "ts" : ISODate("2014-11-25T10:03:53.742Z")
    },
    "context_domain" : "http://www.booxmedia.com/"
}
```
