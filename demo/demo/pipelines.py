# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from qiniu import Auth, put_file
import logging


class DemoPipeline:
    def process_item(self, item, spider):
        return item


class SaveToQiniuPipeline:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            ak=crawler.settings.get('QINIU_AK', ''),
            domain=crawler.settings.get('QINIU_DOMAIN', ''),
            bucket=crawler.settings.get('QINIU_BUCKET', 'demo'),
            sk=crawler.settings.get('QINIU_SK', ''),
            delete_when_finish=crawler.settings.getbool('QINIU_DEL_SRC', False),
            fields=crawler.settings.getlist('QINIU_FIELDS', []),
        )

    def process_item(self, item, spider):
        if self.ak:
            for field in self.fields:
                try:
                    val = item[field]
                except:  # noqa
                    pass
                else:
                    if val.startswith('./'):
                        val = val[2:]
                    q = Auth(self.ak, self.sk)
                    token = q.upload_token(self.bucket, val, 3600)
                    ret, info = put_file(token, val, val)
                    if info.status_code == 200:
                        item[field] = f'http://{self.domain}/{val}'
                        logging.debug(f"success to put file to qiniu: ret={ret} info={info}")
                        public_url = q.private_download_url(item[field], 3600)
                        logging.debug(f'public url is: {public_url}')
                    else:
                        logging.error(f"fail to put file to qiniu: ret={ret} info={info}")
        return item
