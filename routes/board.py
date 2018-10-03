from flask import (
    g,
    abort,
    url_for,
    request,
    redirect,
    Blueprint,
    render_template,
)

from models.board import Board

main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    u = g.current_user
    if u.is_admin():
        bs = Board.all()
        return render_template(
            'board/admin_index.html',
            user=u,
            boards=bs
        )
    else:
        abort(401)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('topic.index'))
