# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 0005 15:48
# @Author  : zhyipeng
# @File    : render.py
import json

from django.http import HttpResponse
from django.conf import settings


def render_json(data=None, code=0):
    '''
    将返回值渲染成json
    :param date: 返回的数据，确保可被序列化
    :param code: 错误码
    :return:
    '''
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG:
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_str = json.dumps(result, ensure_ascii=False, separators=[',', ':'])

    return HttpResponse(json_str)
