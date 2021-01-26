# Pipeline to Download PDF or Save page as PDF for scrapy item


## Installation

Install `scrapy-save-as-pdf` using `pip`:

```
pip install scrapy-save-as-pdf
```

## Configuration
0. _(Optionally)_ if you want to use `WEBDRIVER_HUB_URL`, you can use `docker` to setup one like this:

```shell script
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-alpha-7-20201119
```
then `WEBDRIVER_HUB_URL` value is `http://docker_host_ip:4444/wd/hub`
and we often debug on local host, so we use `http://127.0.0.1:4444/wd/hub`

1. Add the  ``settings.py`` of your Scrapy project like this:

```python
PROXY = ""
CHROME_DRIVER_PATH ='/snap/bin/chromium.chromedriver'
PDF_SAVE_PATH = "./pdfs"
PDF_SAVE_AS_PDF = False
PDF_DOWNLOAD_TIMEOUT = 60
PDF_PRINT_OPTIONS = {
    'landscape': False,
    'displayHeaderFooter': False,
    'printBackground': True,
    'preferCSSPageSize': True,
}
WEBDRIVER_HUB_URL = 'http://127.0.0.1:4444/wd/hub'
```

If both `WEBDRIVER_HUB_URL` and `CHROME_DRIVER_PATH` are set, we use `WEBDRIVER_HUB_URL`.

2. Enable the pipeline by adding it to ``ITEM_PIPELINES`` in your ``settings.py`` file and changing priority:
   
```python
ITEM_PIPELINES = {
    'scrapy_save_as_pdf.pipelines.SaveAsPdfPipeline': -1,
}
```
The order should before your persist pipeline such as save to database and after your preprocess pipeline.

In the demo scrapy project, I put the `SaveToQiniuPipeline` after this plugin to persist pdf to the cloud.

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