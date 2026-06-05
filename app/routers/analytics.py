from fastapi import APIRouter, Depends, HTTPException
from app.models.company import Company
from app.models.price import Price
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_, or_
from app.schemas import StockNearYearHigh, SectorsByRevGrowth, StocksByPriceMomentum, StocksByEarningsGrowth, StocksByAnalystConsensus, StocksByVolume, SectorsAverages
from app.redis_client import r
import json
router_analytics = APIRouter()

@router_analytics.get("/analytics/stocks/near-52-week-high", response_model=list[StockNearYearHigh])
def get_stocks_52wk_high(limit, db: Session = Depends(get_db)):
    data = db.query(Company.name, Company.ticker, Company.current_price, Company.week52_high
                    ).filter(Company.week52_high - Company.current_price < (Company.week52_high * 0.05)
                    ).group_by(Company.name, Company.ticker).limit(limit).all()
    stocks = []
    for row in data:        
        stocks.append({"company": row[0], "ticker": row[1], "current_price": row[2], "week_52high": row[3]})
    if not stocks:
        raise HTTPException(status_code=404, detail="Item not found")
    return stocks

@router_analytics.get("/analytics/sectors/strongest-revenue-growth", response_model=list[SectorsByRevGrowth])
def get_sectors_rev_growth(db: Session = Depends(get_db)):
    cache_key = "analytics:by_revenue"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error {e}")
        res = None
    if res is None:
        data = db.query(Company.sector, func.avg(Company.revenue_growth)
                        ).group_by(Company.sector).order_by(func.avg(Company.revenue_growth).desc()).limit(10).all()
        sectors = []
        for row in data:
            sectors.append({"sector": row[0], "revenue_growth": (row[1] * 100)})
        info = json.dumps(sectors)
        try:
            r.set(cache_key, info, ex=3600)
        except Exception:
            pass
    else:
        sectors = json.loads(res)
    if not sectors:
        raise HTTPException(status_code=404, detail="Item not found")
    return sectors
@router_analytics.get("/analytics/stocks/highest-price-momentum", response_model=list[StocksByPriceMomentum])
def get_stocks_price_momentum(db: Session = Depends(get_db)):
    cache_key = "analytics:by_momentum"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error {e}")
        res = None
    if res is None:
        date_30 = db.query(Price.date).filter(Price.date >= func.now() - text("interval '30 days'")).order_by(Price.date.asc()).limit(1).subquery()
        thirty = db.query(Price.ticker, Company.name, date_30, Price.close_price, Company.current_price
                        ).filter(Price.ticker == Company.ticker
                        ).join(date_30, date_30.c.date == Price.date).group_by(Price.ticker, Company.name, date_30.c.date, Price.close_price, Company.current_price).order_by((((Company.current_price - Price.close_price) / Price.close_price) * 100).desc()).all()
        date_60 = db.query(Price.date).filter(Price.date >= func.now() - text("interval '60 days'")).order_by(Price.date.asc()).limit(1).subquery()
        sixty = db.query(Price.ticker, Company.name, date_60, Price.close_price, Company.current_price
                        ).filter(Price.ticker == Company.ticker
                        ).join(date_60, date_60.c.date == Price.date).group_by(Price.ticker, Company.name, date_60.c.date, Price.close_price, Company.current_price).order_by((((Company.current_price - Price.close_price) / Price.close_price) * 100).desc()).all()
        date_90 = db.query(Price.date).filter(Price.date >= func.now() - text("interval '90 days'")).order_by(Price.date.asc()).limit(1).subquery()
        ninety = db.query(Price.ticker, Company.name, date_90, Price.close_price, Company.current_price
                        ).filter(Price.ticker == Company.ticker
                            ).join(date_90, date_90.c.date == Price.date).group_by(Price.ticker, Company.name, date_90.c.date, Price.close_price, Company.current_price).order_by((((Company.current_price - Price.close_price) / Price.close_price) * 100).desc()).all()
        stocks = dict()
        for row in thirty:
            price_momentum_30 = ((row[4] - row[3]) / row[3]) * 100
            stocks[row[0]] = {"ticker": row[0], "company": row[1], "price_momentum_30": price_momentum_30}
        for row in sixty:
            price_momentum_60 = ((row[4] - row[3]) / row[3]) * 100
            stocks[row[0]]["price_momentum_60"] = price_momentum_60
        for row in ninety:
            price_momentum_90 = ((row[4] - row[3]) / row[3]) * 100
            stocks[row[0]]["price_momentum_90"] = price_momentum_90
        data = json.dumps(stocks)
        try:
            r.set(cache_key, data, ex=3600)
        except Exception:
            pass
    else:
        stocks = json.loads(res)
    if not stocks:
        raise HTTPException(status_code=404, detail="Item not found")
    return list(stocks.values())
    
@router_analytics.get("/analytics/stocks/highest-earnings-growth", response_model=list[StocksByEarningsGrowth])
def get_stocks_earnings_growth(limit = 10, db: Session = Depends(get_db)):
    data = db.query(Company.ticker, Company.name, Company.earnings_growth).filter(Company.earnings_growth.is_not(None)).group_by(Company.ticker, Company.name, Company.earnings_growth).order_by(Company.earnings_growth.desc()).limit(limit).all()
    stocks = []
    for row in data:
        stocks.append({"ticker": row[0], "company": row[1], "earnings_growth": row[2] * 100})
    return stocks
@router_analytics.get("/analytics/sectors/averages", response_model=list[SectorsAverages])
def get_sector_averages(db: Session = Depends(get_db)):
    data = db.query(Company.sector, func.avg(Company.trailing_pe), func.avg(Company.revenue_growth)
                    ).group_by(Company.sector).all()
    sectors = []
    for row in data:
        sectors.append({"sector": row[0], "avg_PE": row[1], "avg_rev_growth": row[2] * 100})
    if not sectors:
        raise HTTPException(status_code=404, detail="item not found")
    return list(sectors)

@router_analytics.get("/analytics/stocks/by-analyst-consensus", response_model=list[StocksByAnalystConsensus])
def get_analyst_consensus(db: Session = Depends(get_db)):
    data = db.query(Company.ticker, Company.current_price, Company.recommendation_key, Company.week52_low
                    ).filter(and_(Company.current_price - Company.week52_low < Company.week52_low * 0.05), or_((Company.recommendation_key == "buy"), Company.recommendation_key == "strong_buy")).all()
    stocks = []
    for row in data:
        stocks.append({"ticker": row[0], "current_price": row[1], "analyst_consensus": row[2]})
    return stocks

@router_analytics.get("/analytics/stocks/volume-anomaly", response_model=list[StocksByVolume])
def get_stocks_high_volume(db: Session = Depends(get_db)):
    cache_key = "analytics:by_volume"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error {e}")
        res = None
    if res is None:
        max_dates = db.query(Price.ticker, func.max(Price.date).label("max_date")).group_by(Price.ticker).subquery()
        vol = db.query(Price.ticker, Price.total_volume).join(max_dates, (Price.ticker == max_dates.c.ticker) & (Price.date == max_dates.c.max_date)).subquery()
        data = db.query(Company.ticker, Company.name, Company.avg_volume, vol
                        ).join(vol, vol.c.ticker == Company.ticker).filter(vol.c.total_volume / Company.avg_volume > 2).group_by(Company.ticker, Company.name, Company.avg_volume, vol.c.ticker, vol.c.total_volume).order_by((vol.c.total_volume / Company.avg_volume).desc()).all()
        stocks = []
        for row in data:
            ratio = row[4] / row[2]
            stocks.append({"ticker": row[0], "company": row[1], "total_volume": row[4], "avg_volume": row[2], "ratio": ratio})
        info = json.dumps(stocks)
        try:
            r.set(cache_key, info, ex=3600)
        except Exception:
            pass
    else:
        stocks = json.loads(res)
    if not stocks:
        raise HTTPException(status_code=404, detail="Item not found")
    return stocks
