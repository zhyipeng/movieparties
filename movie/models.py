from django.db import models
import datetime


class Movie(models.Model):
    '''电影模型'''
    name = models.CharField(max_length=64)
    score = models.CharField(max_length=8, default='0')
    img_url = models.CharField(max_length=256)
    release_date = models.DateField()
    is_hot = models.BooleanField(default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score,
            'img_url': self.img_url,
            'is_hot': self.is_hot,
            'release_date': self.release_date.strftime('%F'),
        }


class BaseCinema(models.Model):
    '''电影院模型'''
    LOCATION = (
        ('荔湾区', '荔湾区'),
        ('黄埔区', '黄埔区'),
        ('天河区', '天河区'),
        ('白云区', '白云区'),
        ('越秀区', '越秀区'),
        ('海珠区', '海珠区'),
        ('从化区', '从化区'),
        ('番禺区', '番禺区'),
        ('花都区', '花都区'),
        ('萝岗区', '萝岗区'),
        ('南沙区', '南沙区'),
        ('增城区', '增城区'),
    )

    location = models.CharField(max_length=32, choices=LOCATION)
    name = models.CharField(max_length=64)

    class Meta:
        # 抽象类，在数据迁移的时候不会创建表
        abstract = True

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'location': self.location
        }


class TppCinema(BaseCinema):
    '''淘票票影院id'''
    tpp_id = models.CharField(max_length=16)

    class Meta:
        db_table = 'tppcinema'


class NmCinema(BaseCinema):
    '''糯米影院id'''
    nm_id = models.CharField(max_length=16)

    class Meta:
        db_table = 'nmcinema'


class TimeCinema(BaseCinema):
    '''时光电影影院id'''
    time_id = models.CharField(max_length=16)

    class Meta:
        db_table = 'timecinema'


class Source(models.Model):
    '''来源'''
    NAME = (
        ('糯米', '糯米'),
        ('时光', '时光'),
        # ('淘票票', '淘票票'),
    )
    name = models.CharField(max_length=8, choices=NAME)


class Schedule(models.Model):
    '''排程表'''
    date = models.DateField()
    start_time = models.CharField(max_length=16)
    end_time = models.CharField(max_length=16)
    language = models.CharField(max_length=16)
    hall = models.CharField(max_length=32)
    price = models.FloatField()
    cinema = models.CharField(max_length=64)

    movie = models.ForeignKey(Movie)
    source = models.ForeignKey(Source)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%F'),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'language': self.language,
            'hall': self.hall,
            'price': self.price,
            'cinema': self.cinema,
            'movie': self.movie.name,
            'source': self.source.name,
        }
