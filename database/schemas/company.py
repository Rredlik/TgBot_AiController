from sqlalchemy import Column, sql, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship

from database.main import TimedBaseModel


class Company(TimedBaseModel):
    __tablename__ = "Company"
    company_id = Column(Integer, primary_key=True, index=True)
    website_id = Column(VARCHAR, unique=True, nullable=False)
    company_name = Column(VARCHAR, nullable=False)
    company_inn = Column(Integer)
    token_balance = Column(Integer, default=0, server_default=u'0')
    def_tokens_in_day = Column(Integer, default=0, server_default=u'0')
    def_tokens_in_month = Column(Integer, default=0, server_default=u'0')

    users = relationship("User", back_populates="company")
    # settings = relationship("CompanySettings", back_populates="company")
    solutions = relationship("CompanySolutions", back_populates="company")

    query: sql.select


# class CompanySettings(TimedBaseModel):
#     __tablename__ = "CompanySettings"
#     id = Column(Integer, primary_key=True, index=True)
#     company_id = Column(Integer, ForeignKey("Company.company_id"))
#     def_tokens_in_day = Column(Integer, default=0, server_default=u'0')
#     def_tokens_in_month = Column(Integer, default=0, server_default=u'0')
#
#     company = relationship("Company", back_populates="settings")
#
#     query: sql.select
