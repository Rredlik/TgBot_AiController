from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, sql

from database.main import TimedBaseModel


class Solution(TimedBaseModel):
    __tablename__ = "Solution"
    solution_id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    small_description = Column(String)
    description = Column(String)
    price = Column(BigInteger, default=0)
    is_active = Column(Boolean, default=True)
    picture = Column(String)

    query: sql.select
