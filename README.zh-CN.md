# 用于下载`pdf`网址或者保存爬取地址为`pdf`的管道（PIPELINE）


## 安装

使用 `pip` 安装包 `scrapy-save-as-pdf`:

```
pip install scrapy-save-as-pdf
```

## 配置
0. _(可选)_ 如果想使用 `WEBDRIVER_HUB_URL`, 可以用如下 `docker`命令构建一个容器:

```shell script
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-alpha-7-20201119
```
`WEBDRIVER_HUB_URL` 就会是`http://docker_host_ip:4444/wd/hub`
而通常我们在本地进行条是,所以值通常是 `http://127.0.0.1:4444/wd/hub`

1. 在`Scrapy`项目的配置文件`settings.py`中添加配置:

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

如果 `WEBDRIVER_HUB_URL` 和 `CHROME_DRIVER_PATH`两个都设置了,会优先使用`WEBDRIVER_HUB_URL`.

2. 在配置文件`settings.py` 中添加此管道(pipline)到 ``ITEM_PIPELINES``变量中:
   
```python
ITEM_PIPELINES = {
    'scrapy_save_as_pdf.pipelines.SaveAsPdfPipeline': -1,
}
```
管道的优先级应该在数据预处理和持久化(比如到数据库)的管道之间

比如在演示`Scrapy`项目中,我在本插件后添加了 `SaveToQiniuPipeline`来把数据存储到七牛云存储中

## 使用

在生成的数据中设置好 `pdf_url` 和(或) `url`等字段
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
`pdf_url` 会被设置为下载号的pdf文件的位置,如果本来就有`pdf_url`字段的值,则会将其移动到`origin_pdf_url`字段,你可以在接下来的管道中处理

## 获取帮助

请使用 `github` 项目提供的工单系统提交工单

## 贡献代码

欢迎提交 `PR` , 我们会尽快讨论合并.