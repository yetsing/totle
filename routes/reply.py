import time

from flask import (
    request,
    url_for,
    redirect,
    Blueprint,
)

from models.message import Messages
from models.topic import Topic
from models.reply import Reply
from models.user import User

from routes import (
    current_user,
    csrf_required,
    login_required,
)

main = Blueprint('reply', __name__)


def users_from_content(content):
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_messages(sender, receivers, reply_link, reply_content):
    content = '你被 {} AT 了，内容：{}'.format(
        sender.username,
        reply_content
    )
    for r in receivers:
        form = dict(
            content=content,
            sender=sender.username,
            receiver=r.username,
            link=reply_link,
        )
        Messages.new(form)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    # 回复链接
    link = request.args.get('link')

    content = form['content']
    users = users_from_content(content)
    r = Reply.add(form, user_id=u.id)
    link += '#id-reply-{}'.format(r.id)
    send_messages(u, users, link, content)

    Topic.update(r.topic_id, active_time=time.time())
    return redirect(url_for('topic.detail', topic_id=r.topic_id))


@main.route('/delete')
@login_required
@csrf_required
def delete():
    reply_id = int(request.args.get('id'))
    r = Reply.delete(id=reply_id)
    return redirect(url_for('topic.detail', topic_id=r.topic_id))