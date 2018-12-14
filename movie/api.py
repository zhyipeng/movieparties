import Levenshtein

from .logic import update_schedule, select_schedule
from lib.render import render_json
from .models import *
from movieparties.error import PARAM_ERROR


def update(request):
    '''
    更新排程
    :param request:
    :return:
    '''
    update_schedule()
    return render_json()


def hot_movies(request):
    '''
    获取热映电影列表
    :param request:
    :return:
    '''
    hot_movie_list = [m.to_dict() for m in Movie.objects.filter(is_hot=True).order_by('-release_date')]
    return render_json(hot_movie_list)


def cinema(request):
    '''
    获取电影院列表
    :param request:
    :return:
    '''
    locations = ('荔湾区', '黄浦区', '天河区', '白云区', '越秀区', '海珠区', '从化区', '番禺区', '花都区', '萝岗区', '南沙区', '增城区')
    result = {}
    for location in locations:
        nm_cinemas = [c.to_dict() for c in NmCinema.objects.filter(location=location)]
        time_cinemas = [c.to_dict() for c in TimeCinema.objects.filter(location=location)]
        res = nm_cinemas[:]
        for tc in time_cinemas:
            for nc in nm_cinemas:
                if Levenshtein.ratio(tc['name'], nc['name']) > 0.65:
                    # print(tc['name'])
                    break
            else:
                res.append(tc)
        result[location] = res
    return render_json(result)


def schedule(request):
    '''
    获取排程
    :param request:
    :return:
    '''
    m_id = int(request.GET.get('m_id'))
    c_id = int(request.GET.get('c_id'))

    if m_id and c_id:
        nm_cinema = NmCinema.objects.filter(id=c_id).first()
        if nm_cinema is None:
            return render_json(code=PARAM_ERROR)
        return render_json(select_schedule(nm_cinema, m_id))

