from app.database import Base
from sqlalchemy import ForeignKey, Column, String, Float, Integer

class Company(Base):
    __tablename__ = "company"

    ticker = Column(String(5), primary_key=True)
    name = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Float)
    trailing_pe  = Column(Float)
    forward_pe = Column(Float)
    week52_high = Column(Float)
    week52_low = Column(Float)
    current_price = Column(Float)
    day50_avg = Column(Float)
    day200_avg = Column(Float)
    revenue_growth = Column(Float)
    earnings_growth = Column(Float)
    recommendation_key = Column(String)
    avg_volume = Column(Integer)
    trailing_eps = Column(Float)
    forward_eps = Column(Float)
     