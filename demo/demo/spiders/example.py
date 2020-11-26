import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = [
        'example.com',
        'http://example.org/',
    ]
    start_urls = [
        'http://example.com/',
        'http://example.org/',
    ]

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css('title::text').get(),
            'content': "\n".join(response.css('body ::text').getall()).strip(),
        }
