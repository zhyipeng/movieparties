# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 0005 14:03
# @Author  : zhyipeng
# @File    : logic.py
import time
from queue import Queue

from lib.p_and_c import Consumer, Producer, Consumer2
from spider import douban
from spider.nm import NmSpider
from spider.timemovie import TimeSpider
from .models import *
from django.core.cache import cache


def update_hot_movie():
    '''
    更新豆瓣热门电影
    :return:
    '''
    hot_movies = list(douban.get_hot_movies())
    hot_movie_names = {m['name'] for m in hot_movies}
    print(hot_movie_names)
    cache.set('douban_hot_movie', hot_movie_names)
    db_movies = Movie.objects.all()
    # 标记非热门电影
    for movie in db_movies:
        if movie.name not in hot_movie_names:
            movie.is_hot = False
            movie.save()
    # 插入新的热门电影
    db_movie_names = {m.name for m in db_movies}
    for hot_movie in hot_movies:
        if hot_movie['name'] not in db_movie_names:
            Movie.objects.create(name=hot_movie['name'], score=hot_movie['score'], img_url=hot_movie['img_url'],
                                 release_date=hot_movie['release_date'])
            print(hot_movie['name'], '已添加')

# @celery_app.task
def update_schedule():
    '''
    更新排程
    :return:
    '''
    nmspider = NmSpider()
    timespider = TimeSpider()
    # 更新热映电影
    nmspider.get_hot_movie()
    timespider.get_hot_movie()
    update_hot_movie()
    # 初始化队列
    nm_cinemas = [(c.nm_id, c.name) for c in NmCinema.objects.all()]
    time_cinemas = [(c.time_id, c.name) for c in TimeCinema.objects.all()]
    nm_cinema_queue = Queue(maxsize=1000)
    time_cinema_queue = Queue(maxsize=1000)
    nm_schedule_queue = Queue(maxsize=1000)
    time_schedule_queue = Queue(maxsize=1000)
    # 初始化生产者
    nm_producer = Producer(nm_cinemas, nm_cinema_queue)
    time_producer = Producer(time_cinemas, time_cinema_queue)
    nm_producer.start()
    time_producer.start()
    # 初始化消费者
    nm_consumers = [Consumer(nmspider, nm_cinema_queue, nm_schedule_queue) for _ in range(2)]
    time_consumers = [Consumer(timespider, time_cinema_queue, time_schedule_queue) for _ in range(5)]
    for i in range(5):
        if i < 2:
            nm_consumers[i].start()
        time_consumers[i].start()

    time.sleep(5)
    # 入库
    Consumer2(nm_schedule_queue).start()
    Consumer2(time_schedule_queue).start()


def select_schedule(cinema, movie_id):
    '''
    查询schedule
    :param cinema: cinemaModel
    :param movie_id:
    :return:
    '''
    date_list = [datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1),
                 datetime.date.today() + datetime.timedelta(days=2)]
    sche_list = Schedule.objects.filter(movie_id=movie_id, cinema=cinema.name, date__in=date_list)
    today = []
    tomorrow = []
    aftertomorrow = []
    for sche in sche_list:
        if sche.date == datetime.date.today():
            if int(sche.start_time[:2]) > datetime.datetime.now().hour:
                today.append(sche.to_dict())
        elif sche.date == date_list[1]:
            tomorrow.append(sche.to_dict())
        elif sche.date == date_list[2]:
            aftertomorrow.append(sche.to_dict())
    return {'today': today, 'tomorrow': tomorrow, 'aftertomorrow': aftertomorrow}
