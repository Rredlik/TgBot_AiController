from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, sql

from database.main import TimedBaseModel


class Dialogs(TimedBaseModel):
    __tablename__ = "Dialogs"
    dialog_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dialog_name = Column(String)
    user_id = Column(BigInteger)
    context = Column(String)


class Requests(TimedBaseModel):
    __tablename__ = "Requests"
    request_id = Column(BigInteger, primary_key=True, autoincrement=True)
    created = Column(BigInteger)
    prompt = Column(String)
    answer = Column(String)
    usage_completion_tokens = Column(BigInteger)
    usage_prompt_tokens = Column(BigInteger)
    usage_total_tokens = Column(BigInteger)

    query: sql.select
