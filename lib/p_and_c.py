#-*- coding: utf-8 -*-
# @Time    : 2018/12/7 0007 15:24
# @Author  : zhyipeng
# @File    : p_and_c.py
import threading
import logging
from movie.models import *


log = logging.getLogger('inf')

class Producer(threading.Thread):
    '''向影院队列插数据'''
    def __init__(self, data, cinema_qu, *args, **kwargs):
        '''

        :param data: [(id, name)]
        :param cinema_qu:
        :param args:
        :param kwargs:
        '''
        super(Producer, self).__init__(*args, **kwargs)
        self.cinema_qu = cinema_qu
        self.data = data


    def run(self):
        for data in self.data:
            self.cinema_qu.put(data)


class Consumer(threading.Thread):
    '''爬虫'''
    def __init__(self, spider, cinema_qu, schedule_qu, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.cinema_qu = cinema_qu
        self.schedule_qu = schedule_qu
        self.spider = spider

    def run(self):
        while 1:
            if self.cinema_qu.empty():
                break
            c_id, name = self.cinema_qu.get()
            schedule_list = self.spider.get_cinema_schedule(c_id)
            for sche in schedule_list:
                sche['cinema'] = name
                self.schedule_qu.put(sche)

class Consumer2(threading.Thread):
    '''存入数据库'''
    def __init__(self, schedule_queue, *args, **kwargs):
        super(Consumer2, self).__init__(*args, **kwargs)
        self.schedule_queue = schedule_queue

    def run(self):
        while 1:
            if self.schedule_queue.empty():
                break
            self.save_schedule(self.schedule_queue.get())


    def save_schedule(self, schedule):
        '''
        保存入库
        :param schedule:
        :return:
        '''
        date = schedule['date']
        start_time = schedule['start_time']
        end_time = schedule['end_time']
        language = schedule['language']
        hall = schedule['hall']
        try:
            price = float(schedule['price'])
        except:
            price = 0
        cinema = schedule['cinema']
        movie_name = schedule['movie']
        source_id = schedule['source']
        movie = Movie.objects.filter(name=movie_name).first()
        if movie is None:
            return
        try:
            Schedule.objects.get_or_create(date=date, start_time=start_time, end_time=end_time, language=language,
                                           hall=hall, price=price, cinema=cinema, movie_id=movie.id,
                                           source_id=source_id)
        except:
            return
        log.info('%s\t%s\t%s\t%s\t%s\t已更新' % (date, start_time, movie_name, cinema, source_id))
