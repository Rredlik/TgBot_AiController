from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, sql

from database.main import BaseModel, TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "User"
    user_id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    website_id = db.Column(String)
    telegram_id = db.Column(String, unique=True)
    telegram_username = db.Column(String(50))
    email = db.Column(String(50), unique=True)
    first_name = db.Column(String(30))
    last_name = db.Column(String(30))
    is_admin = db.Column(Boolean, default=False)
    is_active = db.Column(Boolean, default=True)
    is_manager = db.Column(Boolean, default=False)
    have_bot = db.Column(Boolean, default=False)
    profile_picture = db.Column(String)
    balance = db.Column(BigInteger, default=0)
    tokens_for_a_day = db.Column(BigInteger, default=0)
    tokens_for_a_month = db.Column(BigInteger, default=0)
    tokens_used_in_day = db.Column(BigInteger, default=0)
    tokens_used_in_month = db.Column(BigInteger, default=0)
    company_id = db.Column(String())
    password = db.Column(String())

    query: sql.select


# class UserRelatedModel(BaseModel):
#     __abstract__ = True
#
#     user_id = Column(
#         db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,
#     )