from scrapy.item import Field, Item


class CrawledWebsiteItem(Item):

    domain = Field()
    url = Field()
    title = Field()
    keywords = Field()
    h1 = Field()
    h2 = Field()
    h3 = Field()
    h4 = Field()
    text = Field()
    words = Field()
