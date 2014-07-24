# Scrapy settings for dirbot project
from django.conf import settings as d_settings

d_settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'db_crawler_index',
            'USER': 'postgres',
            'PASSWORD': 'A4ie0pgip3h4yW5XKePHLhAg8',
            'HOST': '',
            'PORT': '',
        }},
    INSTALLED_APPS=(
        'dirbot',
    )
)

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = {
    'dirbot.pipelines.FilterPipeline': 1,
    'dirbot.pipelines.DjangoPipeline': 200,
    }

DOWNLOAD_TIMEOUT = 180 # 3mins
DOWNLOAD_DELAY = 2 # 2 sec
DEPTH_LIMIT = 1
DEPTH_STATS = True
DNSCACHE_ENABLED = True
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'dirbot.middleware.ProxyMiddleware': 1,
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
}
