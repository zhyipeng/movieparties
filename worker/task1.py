# -*- coding: utf-8 -*-
# @Time    : 2018/12/8 0008 10:58
# @Author  : zhyipeng
# @File    : task1.py
from worker import celery_app
from movie.logic import update_schedule


# @celery_app.task
# def test():
#     print(Movie.objects.get(id=1).name)

@celery_app.task
def run_spider():
    update_schedule()