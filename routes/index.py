from flask import (
    Blueprint,
    render_template,
    send_from_directory
)


main = Blueprint('index', __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)