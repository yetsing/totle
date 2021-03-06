import os
import time
import uuid

from flask import (
    g,
    flash,
    abort,
    jsonify,
    request,
    url_for,
    session,
    redirect,
    Blueprint,
    render_template,
    send_from_directory,
)

from models.collection import Collection
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import (
    sort_by_time,
    login_required,
    captcha_required,
    last_login_failed,
)
from cache import cache as client
from routes.helper import create_captcha_image


main = Blueprint('user', __name__)


@main.route('/register/view')
def register_view():
    return render_template('user/register.html')


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    u = User.register(form)
    if u is None:
        flash('注册失败，请您更换用户名')
        return redirect(url_for('.register_view'))
    else:
        flash('注册成功，您现在可以登录')
        return redirect(url_for('.login_view'))


@main.route('/login/view')
def login_view():
    captcha_id = -1
    if last_login_failed():
        captcha_id = client.incr('captcha_id', 1000)
    return render_template(
        'user/login.html',
        captcha_id=captcha_id,
    )


@main.route("/login", methods=['POST'])
@captcha_required
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        ip = request.headers["X-Real-IP"]
        client.set(ip, 'fail', ex=7200)
        flash('登录失败，用户名或密码错误')
        return redirect(url_for('.login_view'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/login/captcha')
def get_captcha():
    captcha_id = request.args['id']
    captcha = create_captcha_image(captcha_id)
    key = 'captcha_id_{}'.format(captcha_id)
    client.set(key, captcha, ex=3600)
    filename = 'captcha_{}.png'.format(captcha_id)
    return send_from_directory('captcha', filename)


@main.route('/logout')
def logout():
    session['user_id'] = -1
    return redirect(url_for('topic.index'))


def created_topic(user_id):
    ts = Topic.all(user_id=user_id)
    sort_by_time(ts)
    return ts


def replied_topic(user_id):
    rs = Reply.all(user_id=user_id)
    ts = []
    visited = set()
    for r in rs:
        t = Topic.one(id=r.topic_id)
        if t.id not in visited:
            visited.add(t.id)
            ts.append(t)
    sort_by_time(ts)
    return ts


@main.route('/user/<username>')
def user_detail(username):
    u = g.current_user
    view_user = User.one(username=username)
    if view_user is None:
        abort(404)
    else:
        created = created_topic(view_user.id)
        replied = replied_topic(view_user.id)
        return render_template(
            'user/profile.html',
            user=u,
            created=created,
            replied=replied,
            view_user=view_user,
        )


@main.route('/user/setting')
def edit():
    u = g.current_user
    result = request.args.get('result', '')
    return render_template('user/setting.html', user=u, result=result)


@main.route('/user/update', methods=['POST'])
def update_setting():
    u = g.current_user
    form = request.form.to_dict()
    form['updated_time'] = int(time.time())
    User.update(u.id, **form)
    flash('设置更改成功')
    return redirect(url_for('.edit'))


@main.route('/user/update/password', methods=['POST'])
def update_password():
    u = g.current_user
    form = request.form.to_dict()
    success = User.change_password(u.id, form)
    if success:
        flash('密码修改成功')
    else:
        flash('密码修改失败，请输入正确的旧密码')
    return redirect(url_for('.edit'))


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file = request.files['avatar']

    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = g.current_user
    User.update(u.id, image='/images/{}'.format(filename))
    flash('头像更改成功')

    return redirect(url_for('.edit'))


def collected_topic(user_id):
    cs = Collection.all(user_id=user_id)
    ts = []
    for c in cs:
        t = Topic.one(id=c.topic_id)
        ts.append(t)
    sort_by_time(ts)
    return ts


@main.route('/user/<username>/collection')
def collection_index(username):
    u = g.current_user
    view_user = User.one(username=username)
    ts = collected_topic(view_user.id)
    return render_template(
        'user/collection.html',
        user=u,
        view_user=view_user,
        collection=ts,
    )


@main.route('/collect/<int:topic_id>')
@login_required
def collect(topic_id):
    u = g.current_user
    u.collect(topic_id)
    d = dict(
        status='success',
    )
    return jsonify(d)


@main.route('/del_collect/<int:topic_id>')
def del_collect(topic_id):
    u = g.current_user
    u.del_collect(topic_id)
    d = dict(
        status='success',
    )
    return jsonify(d)
