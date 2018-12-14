# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 0006 18:24
# @Author  : zhyipeng
# @File    : timemovie.py
import datetime
import json
import Levenshtein
import requests
import logging

from movie.models import TimeCinema
from django.core.cache import cache

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}
log = logging.getLogger('inf')


class TimeSpider:
    '''时光电影爬虫'''

    def __init__(self):
        # self.spider = ChromeSelenium()
        pass

    def get_hot_movie(self):
        '''
        获取时光热门电影
        :return: dict, 最热id
        '''
        url = 'https://m.mtime.cn/Service/callback.mi/Showtime/LocationMovies.api?locationId=365&t=201812619524213966'
        res = requests.get(url=url, params={'locationId': 365}, headers=headers, verify=False)
        try:
            resp_data = json.loads(res.text)
        except json.JSONDecodeError:
            return {'error': 'Json解码失败，请更新爬虫'}
        movie_info_list = resp_data.get('ms')
        hot_movies = {movie.get('tCn'): movie.get('id') for movie in movie_info_list if movie.get('tCn')}
        hotest_id = movie_info_list[0].get("id")
        cache.set("time_hot_movies", hot_movies)
        cache.set("time_hotest_id", hotest_id)


    def get_cinema_id(self):
        '''
        获取影院信息
        :return: dict
        '''
        locations = {
            1401: '番禺区',
            1403: '海珠区',
            1404: '花都区',
            1405: '荔湾区',
            1406: '天河区',
            1407: '越秀区',
            3388: '白云区',
            3389: '黄浦区',
            3390: '南沙区',
            3391: '萝岗区',
            3392: '增城区',
            3393: '从化区',
        }
        url = 'https://ticket-m.mtime.cn/api/proxy/ticket/Showtime/LocationMovieShowtimes.api?locationId=365&movieId=250056&date=20181206&locationId=365&movieId=250056&date=20181206&_=1544094215833'
        data = {
            'locationId': 365,
            'movieId': 250056,
            'date': 20181206,
            '_': 1544094215833,
        }
        res = requests.get(url, headers=headers, params=data)
        try:
            resp_data = json.loads(res.text)
        except json.JSONDecodeError:
            return {'error': 'Json解码失败，请更新爬虫'}
        cinema_info_list = resp_data.get('cs')
        cinema_list = []
        for cinema_info in cinema_info_list:
            cinema = {}
            cinema['time_id'] = cinema_info.get('cid')
            cinema['name'] = cinema_info.get('cn')
            cinema['location'] = locations.get(cinema_info.get('districtId')) or '广州市'
            cinema_list.append(cinema)
        return cinema_list

    def get_cinema_schedule(self, cinema_id):
        '''
        获取影院排程
        :param cinema_id:
        :return: list
        '''
        hot_movies, hotest_id = cache.get("time_hot_movies"), cache.get("time_hotest_id")
        url = 'https://ticket-api-m.mtime.cn/cinema/showtime.api?t=201812620113725916&cinemaId=%s' % str(cinema_id)
        res = requests.get(url=url, headers=headers)
        try:
            resp_data = json.loads(res.text)
        except json.JSONDecodeError:
            return {'error': 'Json解码失败，请更新爬虫'}
        showtimes = resp_data.get('data').get('showtimes')
        result = []
        for showtime in showtimes:
            schedule_list = showtime.get('list')
            movie_id = showtime.get('movieId')
            if int(movie_id) not in hot_movies.values():
                continue
            douban_hot_movie = cache.get("douban_hot_movie")
            m_name = dict(zip(hot_movies.values(), hot_movies.keys())).get(int(movie_id))
            # 跳过不在豆瓣热映的电影
            if douban_hot_movie is not None:
                for douban in douban_hot_movie:
                    # 通过Levenshtein匹配统一电影标题
                    if Levenshtein.ratio(m_name, douban) > 0.7:
                        m_name = douban
                        break
                else:
                    continue

            try:
                date = showtime.get('moviekey').split('_')[1]
            except:
                print(showtime.get('moviekey'))
                continue
            for sche in schedule_list:
                start_time = self.format_time(sche.get("showDay"))
                length = int(sche.get("length"))
                end_time = self.format_time(sche.get("showDay"), length=length)
                language = sche.get("versionDesc") or 'unknow'
                hall = sche.get("hall") or 'unknow'
                price = sche.get("price") or 'unknow'
                movie = m_name
                source = 2
                schedule = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'language': language,
                    'hall': hall,
                    'price': price,
                    'movie': movie,
                    'source': source,
                    'date': date,
                    'cinema': cinema_id,
                }
                result.append(schedule)
                log.info('时光网%s\t%s\t%s\t已爬取' %(date, start_time, movie))
        return result


    @staticmethod
    def format_time(unix_time, length=0):
        '''
        将时间戳转换为北京时间
        :param unix_time: 时间戳
        :return: %H:%M
        '''
        bjtime = datetime.datetime.utcfromtimestamp(int(unix_time)) + datetime.timedelta(hours=8) + datetime.timedelta(minutes=length)
        return bjtime.strftime('%H:%M')


    def insert_cinema_to_db(self):
        '''

        :return:
        '''
        time_cinemas = self.get_cinema_id()

        for cinema in time_cinemas:
            TimeCinema.objects.get_or_create(location=cinema['location'], name=cinema['name'],
                                             time_id=cinema['time_id'])
            print(cinema['name'], '已插入timecinema')


if __name__ == '__main__':
    spider = TimeSpider()
    # spider.get_cinema_id()
    print(spider.get_hot_movie())
