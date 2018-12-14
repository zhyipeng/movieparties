# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 0004 17:08
# @Author  : zhyipeng
# @File    : db.py
import requests, re, os, sys
from lxml import etree

import django

# 设置环境

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieparties.settings")
django.setup()

from movie.models import Source
from spider.nm import NmSpider
from spider.timemovie import TimeSpider

nmspider = NmSpider()
timespider = TimeSpider()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

#
# def get_cinema_info(location=''):
#     url = 'https://www.taopiaopiao.com/showDetailSchedule.htm?city=440100'
#     params = {
#         'showId': '226415',
#         'regionName': location,
#         'ts': '1543915047127',
#         'n_s': 'new',
#     }
#
#     tppheaders = headers
#     tppheaders['referer'] = 'https://www.taopiaopiao.com/showDetail.htm?spm=a1z21.6646385.city.4.678e10d6579JSz&showId=226415&n_s=new&city=440100'
#     # tppheaders['cookie'] = 'dnk=%5Cu9E4F%5Cu7A0B%5Cu4E07%5Cu91CC3743; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie14=UoTYNcK3qRd5vg%3D%3D; t=6733ac96e48ea3cae40f33128973edd8; tracknick=%5Cu9E4F%5Cu7A0B%5Cu4E07%5Cu91CC3743; lid=%E9%B9%8F%E7%A8%8B%E4%B8%87%E9%87%8C3743; csg=e5425b0b; _tb_token_=e9e653ea73515; cookie2=2d21d344ca6a26f6369a3802583aa8a9; cna=m86CFCbhSAwCAT2QYZELIhxY; tb_city=440100; tb_cityName="uePW3Q=="; isg=BB0dKyudHbqN-PmWdS_U7QpTLPkdOWPgieKqC9_n6HQEljvIp4q8XD9AxMo1VmlE'
#     res = requests.get(url=url, headers=tppheaders, params=params)
#     with open('1.html', 'w') as f:
#         f.write(res.text)
#     d_tree = etree.HTML(res.text)
#     url_list = d_tree.xpath('//ul[@class="filter-select"]/li[2]/div[@class="select-tags"]/a/@data-param')
#     name_list = d_tree.xpath('//ul[@class="filter-select"]/li[2]/div[@class="select-tags"]/a/text()')
#     id_list = [re.findall(r'&cinemaId=(\d+)&', href)[0] for href in url_list]
#     return {name_list[i]: id_list[i] for i in range(len(name_list))}

#
# def insert_tpp_cinema():
#     LOCATION = (
#         '', '荔湾区', '黄埔区', '天河区', '白云区', '越秀区', '海珠区',
#         '从化区', '番禺区', '花都区', '萝岗区', '南沙区', '增城区',
#     )
#     for location in LOCATION:
#         for name, c_id in get_cinema_info(location).items():
#             TppCinema.objects.get_or_create(location=location, name=name, tpp_id=c_id)




def insert_source():
    Source.objects.get_or_create(name='糯米')
    Source.objects.get_or_create(name='时光')


if __name__ == '__main__':
    insert_source()
    nmspider.insert_cinema_to_db()
    timespider.insert_cinema_to_db()
    pass
