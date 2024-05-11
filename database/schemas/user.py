from sqlalchemy import Column, String, Boolean, sql, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship
import sqlalchemy as sa

from database.main import TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, index=True)
    website_id = db.Column(VARCHAR, unique=True, nullable=False)
    telegram_id = db.Column(VARCHAR, unique=True)
    telegram_username = db.Column(VARCHAR)
    email = db.Column(VARCHAR, unique=True)
    first_name = db.Column(VARCHAR)
    last_name = db.Column(VARCHAR)
    is_admin = db.Column(Boolean, default=False, server_default=sa.sql.false())
    is_active = db.Column(Boolean, default=True, server_default=sa.sql.true())
    is_manager = db.Column(Boolean, default=False, server_default=sa.sql.false())
    have_bot = db.Column(Boolean, default=False, server_default=sa.sql.false())
    profile_picture = db.Column(VARCHAR)
    balance = db.Column(Integer, default=0, server_default=u'0')
    tokens_for_a_day = db.Column(Integer, default=0, server_default=u'0')
    tokens_for_a_month = db.Column(Integer, default=0, server_default=u'0')
    tokens_used_in_day = db.Column(Integer, default=0, server_default=u'0')
    tokens_used_in_month = db.Column(Integer, default=0, server_default=u'0')
    company_id = db.Column(Integer, ForeignKey("Company.company_id"))
    password = db.Column(VARCHAR)

    company = relationship("Company", back_populates="users")
    dialogs = relationship("Dialogs", back_populates="user")

    query: sql.select


# class UserRelatedModel(BaseModel):
#     __abstract__ = True
#
#     user_id = Column(
#         db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,
#     )