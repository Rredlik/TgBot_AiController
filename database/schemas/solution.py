from sqlalchemy import Column, String, Boolean, sql, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
import sqlalchemy as sa

from database.main import TimedBaseModel


class Solutions(TimedBaseModel):
    __tablename__ = "Solution"
    solution_id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR)
    small_description = Column(VARCHAR)
    description = Column(VARCHAR)
    price = Column(Integer, default=0, server_default=u'0')
    is_active = Column(Boolean, default=True, server_default=sa.sql.true())
    picture = Column(String)

    companies = relationship("Company", back_populates="solution")

    query: sql.select


class CompanySolution(TimedBaseModel):
    __tablename__ = "CompanySolutions"
    id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey("Solution.solution_id"))
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    individual_price = Column(Integer)
    query: sql.select