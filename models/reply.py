from sqlalchemy import Column, Integer, UnicodeText

from models.base_model import db, SQLMixin
from models.user import User


class Reply(SQLMixin, db.Model):

    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        m = Reply.new(form)
        return m

    @classmethod
    def delete(cls, reply):
        db.session.delete(reply)
        db.session.commit()


