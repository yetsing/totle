from flask import Flask

import secret
from models.base_model import db

from routes import (
    from_now,
    format_time,
    current_user,
    new_csrf_token
)

from routes.index import main as index_routes
from routes.user import main as user_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes, mail


def configured_app():
    app = Flask(__name__)
    app.secret_key = secret.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/club?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    mail.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    app.before_request(current_user)
    app.before_request(new_csrf_token)

    app.register_blueprint(index_routes)
    app.register_blueprint(user_routes, url_prefix='/club')
    app.register_blueprint(topic_routes, url_prefix='/club/topic')
    app.register_blueprint(reply_routes, url_prefix='/club/reply')
    app.register_blueprint(board_routes, url_prefix='/club/board')
    app.register_blueprint(mail_routes, url_prefix='/club/message')

    app.template_filter()(format_time)
    app.template_filter()(from_now)


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
