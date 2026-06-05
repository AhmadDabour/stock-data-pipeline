from pydantic import BaseModel

class StockNearYearHigh(BaseModel):
    company: str
    ticker: str
    current_price: float
    week_52high: float

class SectorsByRevGrowth(BaseModel):
    sector: str
    revenue_growth: float

class StocksByPriceMomentum(BaseModel):
    ticker: str
    company: str
    price_momentum_30: float
    price_momentum_60: float
    price_momentum_90: float

class SectorsAverages(BaseModel):
    sector: str
    avg_PE: float
    avg_rev_growth: float

class StocksByEarningsGrowth(BaseModel):
    ticker: str
    company: str
    earnings_growth: float

class StocksByAnalystConsensus(BaseModel):
    ticker: str
    current_price: float
    analyst_consensus: str

class StocksByVolume(BaseModel):
    ticker: str
    company: str
    total_volume: int
    avg_volume: int
    ratio: float