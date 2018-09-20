from models.base_model import SQLMixin, db
from sqlalchemy import Column, String, Integer


class Token(SQLMixin, db.Model):
    token = Column(String(36), nullable=False)
    user_id = Column(Integer, nullable=False)
