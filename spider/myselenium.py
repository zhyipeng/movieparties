#-*- coding: utf-8 -*-
# @Time    : 2018/12/6 0006 18:25
# @Author  : zhyipeng
# @File    : myselenium.py
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.conf import settings

class ChromeSelenium:
    '''无界面浏览器'''
    def __init__(self):
        # 配置chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"')
        # chrome驱动
        driver = os.path.join(settings.BASE_DIR, 'spider', 'chromedriver')

        self.browser = webdriver.Chrome(executable_path=driver, chrome_options=chrome_options)

    def get_resource(self, url, sleep=1):
        '''
        发送请求，获取页面源代码
        :param url: 请求url
        :param sleep: 等待时间
        :return: str
        '''
        self.browser.get(url)
        time.sleep(sleep)
        return self.browser.page_source

