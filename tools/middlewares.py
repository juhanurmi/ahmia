from scrapy.conf import settings

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "test_services_spider":
            request.meta["proxy"] = settings.get("HTTP_PROXY")
