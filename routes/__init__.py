import time
import uuid
from functools import wraps

from flask import (
    g,
    abort,
    flash,
    url_for,
    session,
    request,
    redirect,
)

from models.user import User
from cache import cache as client


def current_user():
    uid = session.get('user_id', '')
    g.current_user = User.one(id=uid)


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        u = g.current_user
        if u is None:
            flash('请登录')
            return redirect(url_for('user.login_view'))
        else:
            return f(*args, **kwargs)

    return decorator


def same_user_required(cls):
    def before_function(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            u = g.current_user
            data = dict(
                GET=request.args,
                POST=request.form,
            )
            mid = int(data[request.method]['id'])
            g.object = cls.one(id=mid)
            if u.id == g.object.user_id:
                return f(*args, *kwargs)
            else:
                abort(401)

        return decorator
    return before_function


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = g.current_user
        if client.exists(token) and u.id == int(client.get(token)):
            client.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = g.current_user
    token = str(uuid.uuid4())
    if u is not None:
        client.set(token, u.id, ex=3600)
    g.token = token


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


# 将时间转化成距今的时间间隔
def from_now(timestamp):
    time_interval = int(time.time()) - timestamp
    second = time_interval + 1
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


# 判断客户端上次是否登录失败
def last_login_failed():
    ip = request.headers["X-Real-IP"]
    return client.exists(ip)


def captcha_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if last_login_failed():
            form = request.form
            captcha = form.get('captcha', '')
            captcha_id = form.get('captcha_id', '')
            key = 'captcha_id_{}'.format(captcha_id)
            if client.exists(key) and captcha.lower() == client.get(key).decode():
                return f(*args, **kwargs)
            else:
                flash('验证码错误')
                return redirect(url_for('.login_view'))
        else:
            return f(*args, **kwargs)

    return wrapper
