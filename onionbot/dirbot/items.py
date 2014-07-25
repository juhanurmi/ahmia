from scrapy.item import Field, Item


class CrawledWebsiteItem(Item):

    id = Field()
    title = Field()
    text = Field()
