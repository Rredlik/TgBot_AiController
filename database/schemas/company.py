from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, sql

from database.main import TimedBaseModel


class Company(TimedBaseModel):
    __tablename__ = "Company"
    company_id = Column(String, primary_key=True, unique=True)
    company_name = Column(String, unique=True)
    company_inn = Column(BigInteger)
    token_balance = Column(BigInteger, default=0)

    query: sql.select


class CompanySettings(TimedBaseModel):
    __tablename__ = "CompanySettings"
    company_id = Column(BigInteger, unique=True)
    def_tokens_in_day = Column(BigInteger, default=0)
    def_tokens_in_month = Column(BigInteger, default=0)

    query: sql.select
