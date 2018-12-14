# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 0004 19:43
# @Author  : zhyipeng
# @File    : nm.py
import datetime
import json
import re
import logging
import threading
from queue import Queue

import Levenshtein
from lxml import etree

from django.core.cache import cache
from movie.models import NmCinema
from spider.myselenium import ChromeSelenium

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

NMHOT = None
log = logging.getLogger('inf')


class NmSpider:
    '''糯米电影爬虫'''

    def __init__(self):
        self.spider = ChromeSelenium()

    def get_hot_movie(self):
        '''
        获取糯米热门电影
        :return: {name: id, name: id, ...}
        '''
        url = 'https://dianying.nuomi.com/common/ranklist?sortType=1&date=1543926258206&channel=&client='
        page = self.spider.get_resource(url)[121:-20]
        # with open('nm_hot.json', 'w', encoding='utf-8') as f:
        #     f.write(page)
        try:
            movies_list = json.loads(page, encoding='urf-8')['data']['movies']
        except json.JSONDecodeError:
            return None
        nm_hot_movies = {movie_dict['movieName']: movie_dict['movieId'] for movie_dict in movies_list}
        cache.set('nm_hot_movies', nm_hot_movies)
        # global NMHOT
        # NMHOT = nm_hot_movies
        return nm_hot_movies

    def get_cinema_id(self):
        '''
        获取糯米电影院id
        :return: {‘白云区':{name:id, name:id, ...}, '天河区':{...}...}
        '''
        arrs = {
            '白云区': 2332,
            '番禺区': 1578,
            '天河区': 1613,
            '海珠区': 2338,
            '荔湾区': 2623,
            '越秀区': 1178,
            '黄浦区': 2007,
            '花都区': 1150,
            '增城区': 2319,
            '从化区': 1585,
            '南沙区': 1986
        }
        res = {}
        for arr in arrs:
            url = 'https://dianying.nuomi.com/movie/cinema?pagelets[]=pageletCinema&reqID=2&cityId=257&pageSize=100&movieId=95395&pageNum=0&areaId=%d' % \
                  arrs[arr]
            page = self.spider.get_resource(url)
            d_tree = etree.HTML(page)
            cinema_name_list = d_tree.xpath('//li//p[1]/span[1]/text()')
            cinema_data_list = d_tree.xpath('//li//a/@data-data')
            cinema_id_list = [re.findall(r'{\\"cinemaId\\":(\d+),', data)[0] for data in cinema_data_list]
            res[arr] = {cinema_name_list[i]: cinema_id_list[i] for i in range(len(cinema_name_list))}
        return res

    def get_cinema_schedule(self, cinema_id):
        '''
        获取一个电影院的所有排程
        :param cinema_id:
        :return:
        '''
        cinema_id = str(cinema_id)
        url = 'https://dianying.nuomi.com/cinema/cinemadetail?cityId=257&cinemaId=%s' % cinema_id
        page = self.spider.get_resource(url)
        d_tree = etree.HTML(page)
        movie_id_list = d_tree.xpath('//div[@id="datelist"]/div/@data-movieid')
        nm_hot_movies = cache.get('nm_hot_movies')
        # nm_hot_movies = NMHOT
        nm_hot_movies_T = dict(zip(nm_hot_movies.values(), nm_hot_movies.keys()))
        result = []
        for m_id in movie_id_list:
            # 跳过不在糯米热映的电影
            if int(m_id) not in nm_hot_movies_T:
                continue
            douban_hot_movie = cache.get("douban_hot_movie")
            m_name = nm_hot_movies_T.get(int(m_id))

            # 跳过不在豆瓣热映的电影
            if douban_hot_movie is not None:  # and m_name not in douban_hot_movie:
                for douban in douban_hot_movie:
                    # 通过Levenshtein匹配统一电影标题
                    if Levenshtein.ratio(m_name, douban) > 0.7:
                        m_name = douban
                        break
                else:
                    continue

            for d_str, d_id in self._get_date_dict(m_id, d_tree).items():
                schedule_list = self._get_schedule(m_id, d_id, d_tree)
                for schedule in schedule_list:
                    schedule['cinema'] = cinema_id
                    schedule['date'] = d_str
                    schedule['movie'] = m_name
                    log.info('糯米电影%s\t%s\t%s\t已爬取' % (d_str, schedule['start_time'], m_name))
                result += schedule_list
        return result

    def _get_schedule(self, movie_id, date_id, d_tree):
        '''
        提取排程
        :param movie_id:
        :param date_id:
        :return: list
        '''
        start_time_list = d_tree.xpath(
            '//div[@data-movieid="%s"]/div[@data-id="%s"]//li//p[@class="start"]/text()' % (movie_id, date_id))
        end_time_xp_list = d_tree.xpath(
            '//div[@data-movieid="%s"]/div[@data-id="%s"]//li//p[2]/text()' % (movie_id, date_id))
        end_time_list = [t[:5] for t in end_time_xp_list]
        language_xp_list = d_tree.xpath(
            '//div[@data-movieid="%s"]/div[@data-id="%s"]//li/div[2]/text()' % (movie_id, date_id))
        language_list = [l.strip() for l in language_xp_list]
        hall = d_tree.xpath('//div[@data-movieid="%s"]/div[@data-id="%s"]//li/div[3]/text()' % (movie_id, date_id))
        price = d_tree.xpath('//div[@data-movieid="%s"]/div[@data-id="%s"]//li//span[2]/text()' % (movie_id, date_id))

        movie = movie_id
        source = 1

        schedule_list = []
        for i in range(len(end_time_list)):
            schedule_item = {
                'start_time': start_time_list[i],
                'end_time': end_time_list[i],
                'language': language_list[i],
                'hall': hall[i],
                'price': price[i],
                'movie': movie,
                'source': source,
            }
            schedule_list.append(schedule_item)
        return schedule_list

    def _get_date_dict(self, movie_id, d_tree):
        '''
        获取日期列表
        :param movie_id:
        :param d_tree:
        :return: {'2018-12-05':d_id, ...}
        '''
        date_list = d_tree.xpath('//div[@data-movieid="%s"]/div[@class="datelist"]/span/text()' % movie_id)
        date_id_list = d_tree.xpath('//div[@data-movieid="%s"]/div[@class="datelist"]/span/@data-id' % movie_id)
        # 格式化 y-m-d
        date_list = list(map(self._format_date, date_list))
        return {date_list[i]: date_id_list[i] for i in range(len(date_list))}

    def _format_date(self, date_str):
        # 今天12月4日
        year = datetime.date.today().year
        month, day = re.findall('(\d+)', date_str)
        return "%d-%02d-%02d" % (year, int(month), int(day))

    def insert_cinema_to_db(self):
        '''
        插入消费队列
        :param qu: Queue
        :return:
        '''
        nm_cinemas = self.get_cinema_id()
        for location, cinema_dict in nm_cinemas.items():
            for name, c_id in cinema_dict.items():
                NmCinema.objects.get_or_create(location=location, name=name, nm_id=c_id)
                print(name, '已插入nmcinema')


if __name__ == '__main__':
    # get_schedule('95395', '563', datetime.date.today())
    # spider = NmSpider()
    # print(spider.get_cinema_schedule('563'))
    pass
