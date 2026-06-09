from app.models import Price
from app.models import Company
from app.database import SessionLocal
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
import yfinance as yf
import datetime

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMZN", "AMD", "INTC", "CRM", "ORCL",
    "JPM", "BAC", "GS", "MS", "WFC", "BLK", "AXP", "C", "SCHW", "COF",
    "JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT", "CVS", "MDT", "AMGN",
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "HAL", "OXY",
    "WMT", "HD", "MCD", "NKE", "SBUX", "TGT", "COST", "PG", "KO", "DIS"
]

def upsert_company(db, ticker, row):
    res = insert(Company).values(
        ticker=ticker,
        sector=row.get("sector"),
        industry=row.get("industry"),
        name=row.get("shortName"),
        market_cap=row.get("marketCap"),
        trailing_pe=row.get("trailingPE"),
        forward_pe=row.get("forwardPE"),
        week52_high=row.get("fiftyTwoWeekHigh"),
        week52_low=row.get("fiftyTwoWeekLow"),
        current_price=row.get("currentPrice"),
        day50_avg=row.get("fiftyDayAverage"),
        day200_avg=row.get("twoHundredDayAverage"),
        revenue_growth=row.get("revenueGrowth"),
        earnings_growth=row.get("earningsGrowth"),
        recommendation_key=row.get("recommendationKey"),
        avg_volume=row.get("averageVolume"),
        trailing_eps=row.get("trailingEps"),
        forward_eps=row.get("forwardEps")
    ).on_conflict_do_update(
        index_elements=["ticker"],
        set_=dict(
            name=row.get("shortName"),
            market_cap=row.get("marketCap"),
            trailing_pe=row.get("trailingPE"),
            forward_pe=row.get("forwardPE"),
            week52_high=row.get("fiftyTwoWeekHigh"),
            week52_low=row.get("fiftyTwoWeekLow"),
            current_price=row.get("currentPrice"),
            day50_avg=row.get("fiftyDayAverage"),
            day200_avg=row.get("twoHundredDayAverage"),
            revenue_growth=row.get("revenueGrowth"),
            earnings_growth=row.get("earningsGrowth"),
            recommendation_key=row.get("recommendationKey"),
            avg_volume=row.get("averageVolume"),
            trailing_eps=row.get("trailingEps"),
            forward_eps=row.get("forwardEps")
        )
    )
    db.execute(res)

def upsert_price(db, ticker, index, row):
    new_price = Price(
        date=index.date(),
        ticker=ticker,
        open_price=float(row["Open"]),
        high_price=float(row["High"]),
        low_price=float(row["Low"]),
        close_price=float(row["Close"]),
        total_volume=int(row["Volume"])
    )
    db.add(new_price)

db = SessionLocal()
for i in TICKERS:
    try:
        ticker = yf.Ticker(i)
        info = ticker.info
        max_date = db.query(func.max(Price.date)).filter(Price.ticker == i).scalar()
        start_date = max_date + datetime.timedelta(days=1) if max_date else None
        df = ticker.history(start=start_date)
        upsert_company(db, i, info)
        for index, row in df.iterrows():
            upsert_price(db, i, index, row)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed on {i} {e}")

db.commit()
