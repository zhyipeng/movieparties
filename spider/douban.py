# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 0004 14:28
# @Author  : zhyipeng
# @File    : douban.py
import re

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


def get_hot_movies():
    '''
    获取豆瓣热映电影
    :return: generater > dict
    img_url
    name
    score
    '''
    url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'

    res = requests.get(url=url, headers=headers)
    d_tree = etree.HTML(res.text)
    movie_img_list = d_tree.xpath('//div[@id="nowplaying"]//li[@class="list-item"]//img/@src')
    movie_name_list = d_tree.xpath(
        '//div[@id="nowplaying"]//li[@class="list-item"]//li[@class="stitle"]/a[@class="ticket-btn"]/@title')
    movie_score_list = d_tree.xpath(
        '//div[@id="nowplaying"]//li[@class="list-item"]//span[@class="subject-rate"]/text()')
    href_list = d_tree.xpath('//div[@id="nowplaying"]//li[@class="list-item"]//li[@class="poster"]/a/@href')
    for i in range(min(len(movie_img_list), len(movie_name_list), len(movie_score_list))):
        item = {}
        item['img_url'] = movie_img_list[i]
        item['name'] = movie_name_list[i].strip()
        item['score'] = movie_score_list[i]
        item['release_date'] = get_release_date(href_list[i])
        yield item


def get_release_date(url):
    '''
    获取上映时间
    :param url:
    :return:
    '''
    res = requests.get(url=url, headers=headers)
    d_tree = etree.HTML(res.text)
    date_str = d_tree.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"][1]/text()')[0]
    print(date_str)
    try:
        return re.findall('\d+-\d+-\d+', date_str)[0]
    except:
        return '0000-00-00'


if __name__ == '__main__':
    # for i in get_hot_movies():
    #     print(i)
    print(get_release_date('https://movie.douban.com/subject/27110296/?from=playing_poster'))
