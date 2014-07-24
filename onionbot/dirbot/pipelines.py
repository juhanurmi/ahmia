from django.db import transaction

from dirbot.models import CrawledWebsite


#from scrapy.exceptions import DropItem



class DjangoPipeline(object):
    def process_item(self, item, spider):
        with transaction.commit_on_success():
            scraps = CrawledWebsite(**item)
            scraps.save()
        return item

class FilterPipeline(object):
    """A pipeline for filtering out items."""

    # MD5sums of the filtered domains
    md5sums = ['example']

    #def process_item(self, item, spider):
        #if domain_md5 in md5sums:
                #raise DropItem("Contains forbidden word: %s" % word)
        #return item
