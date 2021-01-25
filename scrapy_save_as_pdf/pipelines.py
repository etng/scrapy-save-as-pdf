from contextlib import closing
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
from hashlib import md5
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from functools import partial


class SaveAsPdfPipeline:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self.save_base_dir:
            os.makedirs(self.save_base_dir, 0o777, True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy=crawler.settings.get('PROXY', ''),
            chromedriver_path=crawler.settings.get('CHROME_DRIVER_PATH', ''),
            hub_url=crawler.settings.get('WEBDRIVER_HUB_URL', ''),
            download_timeout=crawler.settings.get('PDF_DOWNLOAD_TIMEOUT', ''),
            save_url_as_pdf=crawler.settings.get('PDF_SAVE_AS_PDF', False),
            print_options=crawler.settings.get('PDF_PRINT_OPTIONS', {}),
            save_base_dir=crawler.settings.get('PDF_SAVE_PATH', "./"),

        )

    def process_item(self, item, spider):
        pdf_url = item.get("pdf_url")
        if pdf_url:
            try:
                item["origin_pdf_url"] = pdf_url
            except:  # noqa
                pass
            item["pdf_url"] = self.download_pdf(pdf_url)
        elif self.save_url_as_pdf:
            item["pdf_url"] = self.save_as_pdf(item.get("url"))
        return item

    @staticmethod
    def hash_url(url) -> str:
        m = md5()
        try:
            m.update(url)
        except:  # noqa
            m.update(url.encode('utf-8'))
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
        if self.hub_url:
            driver = webdriver.Remote(
                command_executor=self.hub_url,
                desired_capabilities=DesiredCapabilities.CHROME,
                keep_alive=True,
                options=webdriver_options,
            )
            if 'executeCdpCommand' not in driver.command_executor._commands:
                driver.command_executor._commands['executeCdpCommand'] = (
                    'POST', '/session/$sessionId/goog/cdp/execute')
            # remote driver dit not has execute_cdp_cmd method, but we use chrome, we can monkey patch it
            driver.execute_cdp_cmd = partial(_execute_cdp_cmd, driver=driver)
        else:
            driver = webdriver.Chrome(self.chromedriver_path, options=webdriver_options)
        driver.get(page_url)
        calculated_print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        }
        calculated_print_options.update(self.print_options)
        # print(calculated_print_options)
        response = driver.execute_cdp_cmd("Page.printToPDF", calculated_print_options)
        driver.quit()
        filename = os.path.join(self.save_base_dir, f'{self.hash_url(page_url)}.pdf')
        with open(filename, "wb") as f:
            f.write(base64.b64decode(response['data']))
        return filename


def _execute_cdp_cmd(cmd, cmd_args, driver=None):
    return driver.execute("executeCdpCommand", {'cmd': cmd, 'params': cmd_args})['value']
