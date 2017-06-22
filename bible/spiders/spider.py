import json
import scrapy
from scrapy.exceptions import CloseSpider


class BibleSpider(scrapy.Spider):
    # NVI: 129 ARA: 1608

    name = 'bible'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_url = 'https://events.bible.com/api/bible/chapter/3.1?id=1608&reference='
        self.start_urls = [
            f'{self.base_url}REV.20'
        ]

    def parse(self, response):
        data = json.loads(response.body)
        text = data['content']

        html = scrapy.http.HtmlResponse(
            response.url,
            body=text,
            encoding='utf-8'
        )

        if 'verses' not in response.meta:
            verses = {}
        else:
            verses = response.meta['verses']

        book = data['reference']['human'].split(" ")[0]
        chapter = data['reference']['usfm'][0].split(".")[1]

        next_chapter = data['next']
        if next_chapter is not None:
            next_chapter = next_chapter['usfm'][0]

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

        if next_chapter is None:
            yield verses
        else:
            yield scrapy.Request(
                f"{self.base_url}{next_chapter}",
                callback=self.parse,
                meta={'verses': verses}
            )
