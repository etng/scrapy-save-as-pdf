from scrapy import cmdline

# debug with this workspace
import sys
sys.path.insert(0, '../')

cmdline.execute(['scrapy', 'crawl', 'example'])
