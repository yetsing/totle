import time
from random import randint

import forgery_py
from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.message import Messages


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS club')
        c.execute('CREATE DATABASE club CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE club')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    # 注册管理员
    form = dict(
        username='admin',
        password='123',
        role='admin',
    )
    User.register(form)

    form = dict(
        username='name',
        password='123',
    )
    u = User.register(form)

    form = dict(
        title='问答',
    )
    b = Board.new(form)

    for i in range(6):
        form = dict(
            created_time=int(time.time()) - randint(9000, 300000),
            username=forgery_py.internet.user_name(True),
            password=forgery_py.lorem_ipsum.word(),
        )
        User.register(form)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown demo',
        content=content,
        board_id=b.id,
    )
    Topic.add(form, u.id)

    user_count = User.query.count()
    for i in range(10):
        u = User.query.offset(randint(0, user_count - 1)).first()
        form = dict(
            created_time=int(time.time()) - randint(5000, 400000),
            views=randint(5, 23),
            title=forgery_py.lorem_ipsum.word(),
            content=forgery_py.lorem_ipsum.sentence(),
            board_id=b.id,
        )
        Topic.add(form, u.id)

    for i in range(10):
        u = User.query.offset(randint(0, user_count - 1)).first()
        u.collect(randint(1, 9))

    topic_count = Topic.query.count()
    for i in range(50):
        u = User.query.offset(randint(0, user_count - 1)).first()
        t = Topic.query.offset(randint(0, topic_count - 1)).first()
        form = dict(
            topic_id=t.id,
            content=forgery_py.lorem_ipsum.sentence()
        )
        Reply.add(form, u.id)

    form = dict(
        content='hello world',
        sender=u.username,
        receiver=u.username,
    )
    Messages.new(form)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
