from flask_mail import Message, Mail
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    flash
)

from routes import current_user, login_required

from models.message import Messages
from models.user import User
from config import admin_mail

main = Blueprint('message', __name__)
mail = Mail()


@main.route("/add", methods=["POST"])
@login_required
def add():
    form = request.form.to_dict()
    receiver = form.get('receiver', '')
    r = User.one(username=receiver)
    if r is None:
        flash('请您输入正确的用户名')
        return redirect(url_for('.index'))
    u = current_user()
    form['sender'] = u.username
    m = Messages.new(form)
    content = form['content'] + '<a>{}</a>'.format(m.link)

    # 发邮件
    m = Message(
        subject='有人给你发消息',
        body=content,
        sender=admin_mail,
        recipients=[r.email]
    )
    mail.send(m)

    flash('消息发送成功')
    return redirect(url_for('.index'))


@main.route('/')
@login_required
def index():
    u = current_user()

    sent_message = Messages.all(sender=u.username, sender_del=False)
    received_message = Messages.all(receiver=u.username, receiver_del=False)
    sent_message.reverse()
    received_message.reverse()

    t = render_template(
        'message/index.html',
        user=u,
        send=sent_message,
        received=received_message,
    )
    return t


@main.route('/view/<int:messages_id>')
@login_required
def delete(messages_id):
    user = request.args.get('user', '')
    Messages.delete_one(messages_id, user)
    return redirect(url_for('.index'))
