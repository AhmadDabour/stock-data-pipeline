from app.database import Base
from sqlalchemy import ForeignKey, Column, String, Float, Integer, Date
from app.models.company import Company

class Price(Base):
    __tablename__ = "price"

    date = Column(Date, primary_key=True, nullable=False)
    ticker = Column(String(5), ForeignKey(Company.ticker), primary_key=True, nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    total_volume = Column(Integer)