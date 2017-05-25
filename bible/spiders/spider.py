import json
import scrapy
from bible.items import Verse


class BibleSpider(scrapy.Spider):
    # NVI: 129 ARA: 1608
    name = 'bible'
    start_urls = [
        'https://events.bible.com/api/bible/chapter/3.1?id=1608&reference=GEN.1'
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
        book, chapter = data['reference']['usfm'][0].split(".")

        for verse in html.css(".verse"):
            number = verse.xpath('@data-usfm').extract_first().split(".")[-1]
            text = verse.css('.content::text').extract()

            if number not in verses:
                verses[number] = Verse(
                    book=book,
                    chapter=chapter,
                    verse=number,
                    text=''
                )
            verses[number]['text'] += ''.join(text).strip()

        yield verses
