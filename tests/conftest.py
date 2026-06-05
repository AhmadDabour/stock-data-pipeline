import pytest
from app.models.company import Company
from app.models.price import Price
from app.database import SessionLocal
from sqlalchemy import text
import datetime

@pytest.fixture(scope="session")
def ingestion():
    db = SessionLocal()
    new_comp = Company(
        ticker="test",
        name="test",
        sector="Technology",
        industry="E-Commerce",
        market_cap=1500000000.0,
        trailing_pe=30.0,
        forward_pe=25.0,
        week52_high=200.0,
        week52_low=150.0,
        current_price=195.0,
        day50_avg=190.0,
        day200_avg=180.0,
        revenue_growth=0.25,
        earnings_growth=0.15,
        recommendation_key="buy",
        avg_volume=1000000,
        trailing_eps=5.0,
        forward_eps=6.0
    )
    new_comp1 = Company(
        ticker="test1",
        name="Apple",
        sector="Technology",
        industry="Consumer Electronics",
        market_cap=2500000000.0,
        trailing_pe=28.0,
        forward_pe=24.0,
        week52_high=180.0,
        week52_low=140.0,
        current_price=146.0,
        day50_avg=160.0,
        day200_avg=155.0,
        revenue_growth=0.10,
        earnings_growth=0.12,
        recommendation_key="strong_buy",
        avg_volume=2000000,
        trailing_eps=6.0,
        forward_eps=7.0
    )
    prices = [
        Price(ticker="test",  date=datetime.date(2026, 5, 25), open_price=190.0, high_price=196.0, low_price=188.0, close_price=194.0, total_volume=5000000),
        Price(ticker="test",  date=datetime.date(2026, 4, 5),  open_price=185.0, high_price=191.0, low_price=183.0, close_price=189.0, total_volume=4500000),
        Price(ticker="test",  date=datetime.date(2026, 3, 6),  open_price=180.0, high_price=186.0, low_price=178.0, close_price=184.0, total_volume=4000000),
        Price(ticker="test1", date=datetime.date(2026, 5, 25), open_price=152.0, high_price=157.0, low_price=150.0, close_price=154.0, total_volume=8000000),
        Price(ticker="test1", date=datetime.date(2026, 4, 5),  open_price=148.0, high_price=153.0, low_price=146.0, close_price=150.0, total_volume=7000000),
        Price(ticker="test1", date=datetime.date(2026, 3, 6),  open_price=144.0, high_price=149.0, low_price=142.0, close_price=146.0, total_volume=6000000),
    ]
    db.add(new_comp)
    db.add(new_comp1)
    for p in prices:
        db.add(p)
    db.commit()
    yield
    db.rollback()
    db.execute(text("TRUNCATE price, company CASCADE"))
    db.commit()
    db.close()
