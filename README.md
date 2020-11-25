# Download PDF function for scrapy


## Installation

Install scrapy-save-as-pdf using pip::

    $ pip install scrapy-save-as-pdf

## Configuration

1. Add the  ``settings.py`` of your Scrapy project like this:

```python
PROXY = ""
CHROME_DRIVER_PATH ='/snap/bin/chromium.chromedriver'
PDF_SAVE_PATH="./pdfs"
PDF_SAVE_AS_PDF = False
PDF_DOWNLOAD_TIMEOUT = 60
PDF_PRINT_OPTIONS = {
    'landscape': False,
    'displayHeaderFooter': False,
    'printBackground': True,
    'preferCSSPageSize': True,
}
```

2. Enable the pipeline by adding it to ``ITEM_PIPELINES`` in your ``settings.py`` file and changing HttpCompressionMiddleware
 priority:
   
```python
ITEM_PIPELINES = {
    'scrapy_save_as_pdf.pipelines.SaveAsPdfPipeline': -1,
}
```
The order should before your persist pipeline such as save to database and after your preprocess pipeline.


## Usage

set the `pdf_url` and/or `url` field in your yielded item
```python
import scrapy

class MySpider(scrapy.Spider):
    start_urls = [
        "http://example.com",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        yield {
            "url": "http://example.com/cate1/page1.html",
            "pdf_url": "http://example.com/cate1/page1.pdf",
        }
        yield {
            "url": "http://example.com/cate1/page2.html",
            "pdf_url": "http://example.com/cate1/page2.pdf",
        }
```
the `pdf_url` field will be populated with the downloaded pdf file location, if `pdf_url` field has old value then move it to `origin_pdf_url` field, you can handle them in your next pipeline.

## Getting help

Please use github issue

## Contributing

PRs are always welcomed.