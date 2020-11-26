# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'demo'

SPIDER_MODULES = ['demo.spiders']
NEWSPIDER_MODULE = 'demo.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'demo.middlewares.DemoSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'demo.middlewares.DemoDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'demo.pipelines.DemoPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

from textwrap import dedent

PROXY = ""
CHROME_DRIVER_PATH = '/snap/bin/chromium.chromedriver'
PDF_SAVE_PATH = "./pdfs"
PDF_SAVE_AS_PDF = True
PDF_DOWNLOAD_TIMEOUT = 60
PDF_PRINT_OPTIONS = {
    'landscape': False,
    'displayHeaderFooter': True,
    'printBackground': True,
    'preferCSSPageSize': True,
    'marginTop': 2,
    'marginBottom': 2,
    'headerTemplate': dedent('''
    <div style="font-size:12px;text-align:center">
        <span class="title" style="color:red"></span>
        (<span class="url"></span>)
    </div>
    '''.strip()),
    'footerTemplate': dedent('''
    <div style="font-size:12px">
        <div style="float:left;width:50%"><span class="date"></span></div> 
        <div style="float:right;text-align:right;width:50%">
            <span class="pageNumber"></span>/<span class="totalPages"></span>
        <div>
    </div>'''.strip()),
}
WEBDRIVER_HUB_URL = ''
PDF_ON_SAVE = 'demo.utils.SaveToQiNiu'
del dedent

ITEM_PIPELINES = {
    'scrapy_save_as_pdf.pipelines.SaveAsPdfPipeline': -1,
    'demo.pipelines.SaveToQiniuPipeline': 0,
}

QINIU_AK = ''
QINIU_SK = ''
QINIU_BUCKET = ''
QINIU_DOMAIN = ''
QINIU_DEL_SRC = True
QINIU_FIELDS = [
    'pdf_url',
]

try:
    from .local_settings import *
except:  # noqa
    pass
