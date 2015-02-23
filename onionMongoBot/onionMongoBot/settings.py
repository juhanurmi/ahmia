# -*- coding: utf-8 -*-

# Scrapy settings for onionMongoBot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'onionMongoBot'

SPIDER_MODULES = ['onionMongoBot.spiders']
NEWSPIDER_MODULE = 'onionMongoBot.spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"

DOWNLOAD_TIMEOUT = 120 # 2 min
DOWNLOAD_DELAY = 2 # 2 sec

# MongoDB settings
ITEM_PIPELINES = [
  'scrapy_mongodb.MongoDBPipeline',
]

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'companies'

MONGODB_ADD_TIMESTAMP = True

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.ProxyMiddleware': 410,
}
