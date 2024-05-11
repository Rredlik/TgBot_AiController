from sqlalchemy import Column, Boolean, sql, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
import sqlalchemy as sa

from database.main import TimedBaseModel


class Dialogs(TimedBaseModel):
    __tablename__ = "Dialogs"
    dialog_id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR)
    context = Column(VARCHAR)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    is_deleted = Column(Boolean, default=False, server_default=sa.sql.false())

    user = relationship("User", back_populates="dialog")
    requests = relationship("Requests", back_populates="dialog")
    query: sql.select


class Requests(TimedBaseModel):
    __tablename__ = "Requests"
    request_id = Column(Integer, primary_key=True, index=True)
    dialog_id = Column(Integer, ForeignKey("Dialogs.dialog_id"))
    # created = Column(BigInteger)
    prompt = Column(VARCHAR)
    answer = Column(VARCHAR)
    usage_completion_tokens = Column(Integer, default=0, server_default=u'0')
    usage_prompt_tokens = Column(Integer, default=0, server_default=u'0')
    usage_total_tokens = Column(Integer, default=0, server_default=u'0')

    dialog = relationship("Dialogs", back_populates="request")

    query: sql.select

