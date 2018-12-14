# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 0007 19:34
# @Author  : zhyipeng
# @File    : config.py
from datetime import timedelta
import django
import os, sys

# 设置环境

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieparties.settings")
django.setup()

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'
# import
CELERY_IMPORTS = (
    'worker.task1',
)
# schedules
CELERYBEAT_SCHEDULE = {
    # 'test_schedule': {
    #     'task': 'worker.task1.test',
    #     'schedule': timedelta(seconds=3),  # 每 3 秒执行一次
    # },
    'spider': {
        'task': 'worker.task1.run_spider',
        'schedule': timedelta(hours=24),  # 每天执行一次
    }
}
