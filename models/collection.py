from sqlalchemy import Column, Integer
from models.base_model import db, SQLMixin


class Collection(SQLMixin, db.Model):
    user_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, nullable=False)
