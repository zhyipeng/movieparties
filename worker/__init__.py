#-*- coding: utf-8 -*-
# @Time    : 2018/12/7 0007 19:34
# @Author  : zhyipeng
# @File    : __init__.py.py

from celery import Celery

celery_app = Celery('movieparties')
celery_app.config_from_object('worker.config')