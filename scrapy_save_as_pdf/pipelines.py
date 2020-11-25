from contextlib import closing
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
from hashlib import md5


class SaveAsPdfPipeline:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy=crawler.settings.get('PROXY', ''),
            chromedriver_path=crawler.settings.get('CHROME_DRIVER_PATH', ''),
            download_timeout=crawler.settings.get('PDF_DOWNLOAD_TIMEOUT', ''),
            save_as_pdf=crawler.settings.get('PDF_SAVE_AS_PDF', False),
            print_options=crawler.settings.get('PDF_PRINT_OPTIONS', {}),
            save_base_dir=crawler.settings.get('PDF_SAVE_PATH', "./"),
        )

    def process_item(self, item, spider):
        if pdf_url := item.get("pdf_url"):
            item["origin_pdf_url"] = pdf_url
            item["pdf_url"] = self.download_pdf(pdf_url)
        elif self.save_as_pdf:
            item["pdf_url"] = self.save_as_pdf(item.get("url"))

    @staticmethod
    def hash_url(url) -> str:
        m = md5()
        m.update(url)
        return m.hexdigest()

    def download_pdf(self, pdf_url) -> str:
        proxies = None
        if self.proxy:
            proxies = {
                'http': self.proxy,
                'https': self.proxy,
            }
        with closing(
                requests.get(pdf_url, stream=True, proxies=proxies, timeout=self.download_timeout)) as response:
            chunk_size = 1024
            filename = os.path.join(self.save_base_dir, f'{self.hash_url(pdf_url)}.pdf')
            with open(filename, "wb") as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
            return filename

    def save_as_pdf(self, page_url):
        webdriver_options = Options()
        webdriver_options.add_argument('--headless')
        if self.proxy:
            webdriver_options.add_argument(f"--proxy-server={self.proxy}")
        webdriver_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(self.chromedriver_path, options=webdriver_options)
        driver.get(page_url)
        calculated_print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        }
        calculated_print_options.update(self.print_options)
        response = driver.execute_cdp_cmd("Page.printToPDF", calculated_print_options)
        driver.quit()
        filename = os.path.join(self.save_base_dir, f'{self.hash_url(page_url)}.pdf')
        with open(filename, "wb") as f:
            f.write(base64.b64decode(response['data']))
        return filename
