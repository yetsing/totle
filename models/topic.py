import time

from sqlalchemy import Integer, Column, UnicodeText, Unicode

from models.base_model import SQLMixin, db
from models.board import Board
from models.user import User
from models.reply import Reply


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)
    active_time = Column(Integer, default=time.time)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        m = Topic.new(form)
        return m

    @classmethod
    def get(cls, topic_id):
        m = cls.one(id=topic_id)
        m.views += 1
        m.save()
        return m

    @classmethod
    def delete(cls, topic):
        replies = topic.replies()
        for r in replies:
            db.session.delete(r)
        db.session.delete(topic)
        db.session.commit()

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def board(self):
        b = Board.one(id=self.board_id)
        return b
