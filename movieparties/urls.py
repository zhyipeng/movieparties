"""movieparties URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from movie.api import *
from movie.views import *


urlpatterns = [
    url(r'^$', index),
    url(r'^movie/(\d+)$', detail),

    url(r'^api/movie/update$', update),
    url(r'^api/movie/hot_movies$', hot_movies),
    url(r'^api/movie/cinema$', cinema),
    url(r'^api/movie/schedule$', schedule),
    # url(r'^api/movie/(\d+)$', detail),
]
