#-*- coding: utf-8 -*-
# @Time    : 2018/12/5 0005 18:37
# @Author  : zhyipeng
# @File    : views.py

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import *


def index(request):
    return render_to_response('index.html')


def detail(request, m_id):
    try:
        movie = Movie.objects.get(id=m_id)
    except:
        return HttpResponseRedirect('/')
    return render(request, 'detail.html', {'movie': movie})