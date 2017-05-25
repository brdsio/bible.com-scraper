import scrapy


class Verse(scrapy.Item):
    book = scrapy.Field()
    chapter = scrapy.Field()
    verse = scrapy.Field()
    text = scrapy.Field()
