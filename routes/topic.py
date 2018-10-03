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
    u = g.current_user
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
    )


@main.route('/<int:topic_id>')
def detail(topic_id):
    u = g.current_user
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
    u = g.current_user
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
    u = g.current_user
    t = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', topic_id=t.id))


@main.route("/delete")
@login_required
@same_user_required(Topic)
@csrf_required
def delete():
    Topic.delete(g.object)
    return redirect(url_for('.index'))


@main.route('/edit')
@login_required
@same_user_required(Topic)
def edit():
    u = g.current_user
    t = g.object
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
@same_user_required(Topic)
@csrf_required
def update():
    form = request.form.to_dict()
    form['updated_time'] = time.time()
    topic_id = int(form.pop('id'))
    Topic.update(g.object, **form)
    return redirect(url_for('.detail', topic_id=topic_id))
