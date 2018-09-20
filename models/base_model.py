import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=time.time)
    updated_time = Column(Integer, default=0)

    @classmethod
    def new(cls, form):
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

        return m

    @classmethod
    def delete(cls, **kwargs):
        m = cls.one(**kwargs)
        db.session.delete(m)
        db.session.commit()

        return m

    @classmethod
    def update(cls, m_id, **kwargs):
        m = cls.query.filter_by(id=m_id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        d = dict()
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d


class SimpleUser(SQLMixin, db.Model):
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


if __name__ == '__main__':
    db.create_all()
    info = dict(
        username='123',
        password='456',
    )
    u = SimpleUser.new(info)
    print(u)
    u = SimpleUser.one(username='123')
    print(u)
