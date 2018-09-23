import time
import uuid
from functools import wraps

from flask import (
    g,
    url_for,
    session,
    request,
    abort,
    redirect,
    flash)

from models.token import Token
from models.user import User
from models.topic import Topic
from utils import log
from cache import cache


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        u = current_user()
        if u is None:
            flash('请登录')
            return redirect(url_for('user.login_view'))
        else:
            return f(*args, **kwargs)

    return decorator


def same_user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        u = current_user()
        data = dict(
            GET=request.args,
            POST=request.form,
        )
        topic_id = int(data[request.method]['id'])
        t = Topic.one(id=topic_id)
        if u.id == t.user_id:
            return f(*args, *kwargs)
        else:
            abort(401)

    return decorator


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        if cache.exists(token) and u.id == int(cache.get(token)):
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    if u is not None:
        cache.set(token, u.id)
    g.token = token


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


# 将时间转化成距今的时间间隔
def from_now(timestamp):
    time_interval = int(time.time()) - timestamp
    second = time_interval
    minute = second / 60
    hour = minute / 60
    day = hour / 24
    month = day / 30
    year = month / 12
    if year > 1:
        return '{} 年前'.format(int(year))
    elif month > 1:
        return '{} 个月前'.format(int(month))
    elif day > 1:
        return '{} 天前'.format(int(day))
    elif hour > 1:
        return '{} 小时前'.format(int(hour))
    elif minute > 1:
        return '{} 分钟前'.format(int(minute))
    else:
        return '{} 秒前'.format(int(second))


def sort_by_time(ms):
    for i in range(1, len(ms)):
        temp = ms[i]
        j = i - 1
        while ms[j].active_time < temp.active_time and j >= 0:
            ms[j + 1] = ms[j]
            j -= 1
        ms[j + 1] = temp
