from scrapy.conf import settings

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "test_services_spider":
            print "THE SPIDER IS TEST SERVICES SPIDER!"
            request.meta["proxy"] = settings.get("HTTP_PROXY")
