import json
import scrapy
from bible.items import Verse


class BibleSpider(scrapy.Spider):
    # NVI: 129 ARA: 1608

    name = 'bible'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_url = 'https://events.bible.com/api/bible/chapter/3.1?id=1608&reference='
        self.start_urls = [
            f'{self.base_url}GEN.1'
        ]

    def parse(self, response):
        data = json.loads(response.body)
        text = data['content']

        html = scrapy.http.HtmlResponse(
            response.url,
            body=text,
            encoding='utf-8'
        )

        verses = {}
        book = data['reference']['human'].split(" ")[0]
        chapter = data['reference']['usfm'][0].split(".")[1]

        for verse in html.css(".verse"):
            number = verse.xpath('@data-usfm').extract_first().split(".")[-1]
            text = verse.css('.content::text').extract()

            if book not in verses:
                verses[book] = {}

            if chapter not in verses[book]:
                verses[book][chapter] = {}

            if number not in verses[book][chapter]:
                verses[book][chapter][number] = ''

            verses[book][chapter][number] += ''.join(text).strip()

        yield verses
