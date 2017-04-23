import scrapy


class Verse(scrapy.Item):
    verse = scrapy.Field()
    text = scrapy.Field()
