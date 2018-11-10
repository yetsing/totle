import hashlib

from sqlalchemy import Column, String

import config
from models.base_model import SQLMixin, db
from models.collection import Collection


class User(SQLMixin, db.Model):
    __tablename__ = 'User'

    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    signature = Column(String(200), default='这家伙很懒，什么个性签名都没有留下')
    image = Column(String(100), nullable=False, default='/images/default.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)
    role = Column(String(10), nullable=False, default='normal')

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        return User.one(**query)

    @classmethod
    def change_password(cls, id, form):
        u = User.one(id=id)
        old_password = form.pop('old_password')
        if u.password == User.salted_password(old_password):
            new_password = form.pop('new_password')
            form['password'] = User.salted_password(new_password)
            User.update(id, **form)
            return True
        else:
            return False

    @staticmethod
    def is_collected(user, topic_id):
        if user is None:
            return False
        c = Collection.one(user_id=user.id, topic_id=topic_id)
        if c is None:
            return False
        else:
            return True

    def collect(self, topic_id):
        if not User.is_collected(self, topic_id):
            form = dict(
                user_id=self.id,
                topic_id=topic_id,
            )
            Collection.new(form)

    def del_collect(self, topic_id):
        if User.is_collected(self, topic_id):
            Collection.delete(user_id=self.id, topic_id=topic_id)

    @property
    def collection_count(self):
        cs = Collection.all(user_id=self.id)
        return len(cs)

    def is_admin(self):
        return self.role == 'admin'
