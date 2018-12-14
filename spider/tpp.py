# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 0004 16:20
# @Author  : zhyipeng
# @File    : tpp.py
import re

import requests
from lxml import etree

from django.core.cache import cache

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置谷歌浏览器支持无界面运行
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = 'chromedriver.exe'

browser = webdriver.Chrome(executable_path=driver, chrome_options=chrome_options)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


def get_tpp_hot_movies():
    url = 'https://www.taopiaopiao.com/showList.htm?n_s=new'
    res = requests.get(url=url, headers=headers)
    d_tree = etree.HTML(res.text)
    movie_name_list = d_tree.xpath(
        '//div[@class="tab-movie-list"][1]//div[@class="movie-card-name"]/span[@class="bt-l"]/text()')
    movie_href_list = d_tree.xpath('//div[@class="tab-movie-list"][1]//a[@class="movie-card-buy"]/@href')
    movie_id_list = [re.findall(r'showId=(\d+)&', href)[0] for href in movie_href_list]
    movie_info = {movie_name_list[i]: movie_id_list[i] for i in range(len(movie_name_list)) if movie_id_list[i]}
    valid_movies = set(movie_name_list) & set(cache.get('movie_list'))
    # for movie_name in valid_movies:
    #     get_schedule(movie_name, )


def get_schedule(movie, location, cinema, date):
    '''
    获取影院排程表
    :param movie: 电影名
    :param location: 区
    :param cinema: 影院
    :param data: 日期
    :return:
    '''
    url = 'https://dianying.taobao.com/showDetail.htm?spm=a1z21.3046609.w2.4.32c0112aiikPAg&showId=226415&n_s=new&source=current'
    loginurl = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fdianying.taobao.com%2FshowDetail.htm%3Fspm%3Da1z21.6646273.w2.5.5c5643302E7RjV%26showId%3D154563%26n_s%3Dnew%26source%3Dcurrent'


    browser.get(loginurl)
    time.sleep(2)

    browser.find_element_by_id("TPL_username_1").send_keys('鹏程万里3743')
    browser.find_element_by_id("TPL_password_1").send_keys('tb951210')
    time.sleep(2)
    browser.find_element_by_id("J_SubmitStatic").click()
    time.sleep(2)

    cookies = browser.get_cookies()

    # res = requests.get(url=url, params=data, headers=headers, proxies=proxies)
    with open('1.html', 'w', encoding='utf-8') as f:
        f.write(browser.page_source)

if __name__ == '__main__':
    get_schedule('', '', '', '')
    # get_tpp_hot_movies()
