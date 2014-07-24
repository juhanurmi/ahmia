======
dirbot
======

This is a Scrapy project to crawl .onion websites from the Tor network.

It requires Tor software (use Tor2web mode) and Privoxy.

Bot is integraded to Django.

Items
=====

The items scraped by this project are websites, and the item is defined in the
class::

    dirbot.items.CrawledWebsiteItem

This is similar to Django model in Django integration
class::

    dirbot.models.CrawledWebsite

See the source code for more details.

Spiders
=======

This project contains one spider called ``OnionSpider`` that you can see by running::

    scrapy list

Spider: OnionSpider
------------

Middlewares
===========

Middlewares define HTTP proxy for .onion domains. 
Note that only .onion domains can be crawled using the HTTP proxy.

Furthermore, non-text responses are filtered out.

Pipelines
=========

This project uses a pipeline to filter out some websites
This pipeline is defined in the 
class::

    dirbot.pipelines.FilterPipeline

The data is passed to Django and Django saves it to Postgresql database.
See
class::

    dirbot.pipelines.DjangoPipeline
