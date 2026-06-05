from app.models import Price
from app.models import Company
from app.database import SessionLocal
import yfinance as yf
import pandas as pd
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMZN", "AMD", "INTC", "CRM", "ORCL",
    "JPM", "BAC", "GS", "MS", "WFC", "BLK", "AXP", "C", "SCHW", "COF",
    "JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT", "CVS", "MDT", "AMGN",
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "HAL", "OXY",
    "WMT", "HD", "MCD", "NKE", "SBUX", "TGT", "COST", "PG", "KO", "DIS"
]
def insert_company(row: dict, db): # yf.info
    new_company = Company(ticker=row.get("symbol"), name=row.get("shortName"), sector=row.get("sector"), industry=row.get("industry"), market_cap=row.get("marketCap"), trailing_pe=row.get("trailingPE"), forward_pe=row.get("forwardPE"), week52_high=row.get("fiftyTwoWeekHigh"), week52_low=row.get("fiftyTwoWeekLow"), current_price=row.get("currentPrice"), day50_avg=row.get("fiftyDayAverage"), day200_avg=row.get("twoHundredDayAverage"), revenue_growth=row.get("revenueGrowth"), earnings_growth=row.get("earningsGrowth"), recommendation_key=row.get("recommendationKey"), avg_volume=row.get("averageVolume"), trailing_eps=row.get("trailingEps"), forward_eps=row.get("forwardEps"))
    db.add(new_company)
def insert_price(index, ticker, row: dict, db): # yf.history
        new_price = Price(date=index.date(), ticker=ticker, open_price=float(row["Open"]), high_price=float(row["High"]), low_price=float(row["Low"]), close_price=float(row["Close"]), total_volume=int(row["Volume"]))
        db.add(new_price)
        
db = SessionLocal()
for i in TICKERS:
    ticker = yf.Ticker(i)
    info = ticker.info
    df = ticker.history(period="5y")
    insert_company(info, db)
    for index, row in df.iterrows():
        insert_price(index, i, row, db)
db.commit()