from sqlalchemy import Column, UnicodeText, String, Boolean

from models.base_model import SQLMixin, db


class Messages(SQLMixin, db.Model):
    content = Column(UnicodeText, nullable=False)
    sender = Column(String(50), nullable=False)
    receiver = Column(String(50), nullable=False)
    sender_del = Column(Boolean, default=False)
    receiver_del = Column(Boolean, default=False)
    link = Column(String(50), default='')

    @classmethod
    def delete_one(cls, m_id, user_del):
        m = Messages.one(id=m_id)
        setattr(m, user_del, True)
        if m.sender_del and m.receiver_del:
            db.session.delete(m)
            db.session.commit()
        else:
            db.session.add(m)
            db.session.commit()
