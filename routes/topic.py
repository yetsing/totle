from flask import (
    Blueprint,
    render_template,
)

from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    sort_by_time(ms)
    bs = Board.all()
    return render_template(
        "topic/index.html",
        user=u,
        ms=ms,
        bs=bs,
        bid=board_id,
        token=g.token,
    )


@main.route('/<int:topic_id>')
def detail(topic_id):
    u = current_user()
    t = Topic.get(topic_id)
    b = Board.one(id=t.board_id)
    collect = User.is_collected(u, t.id)
    return render_template(
        "topic/detail.html",
        user=u,
        topic=t,
        board=b,
        token=g.token,
        collect=collect,
    )


@main.route("/new")
@login_required
def new():
    u = current_user()
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    return render_template(
        "topic/new.html",
        user=u,
        bs=bs,
        bid=board_id,
        token=g.token,
    )


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', topic_id=t.id))


@main.route("/delete")
@login_required
@same_user_required
@csrf_required
def delete():
    topic_id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, topic_id)
    Topic.delete(topic_id)
    return redirect(url_for('.index'))


@main.route('/edit')
@login_required
@same_user_required
def edit():
    u = current_user()
    topic_id = int(request.args.get('id'))
    t = Topic.one(id=topic_id)
    bs = Board.all()
    return render_template(
        'topic/edit.html',
        bs=bs,
        user=u,
        topic=t,
        token=g.token,
    )


@main.route('/update', methods=['POST'])
@login_required
@same_user_required
@csrf_required
def update():
    form = request.form.to_dict()
    form['updated_time'] = time.time()
    topic_id = int(form.pop('id'))
    Topic.update(topic_id, **form)
    return redirect(url_for('.detail', topic_id=topic_id))
