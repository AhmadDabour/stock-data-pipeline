from app.main import app
from fastapi.testclient import TestClient
call = TestClient(app)
def test_by_high(ingestion):
    response = call.get("/analytics/stocks/near-52-week-high?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "company" in data[0]

def test_by_rev(ingestion):
    response = call.get("/analytics/sectors/strongest-revenue-growth")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "sector" in data[0]

def test_by_momentum(ingestion):
    response = call.get("/analytics/stocks/highest-price-momentum")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "ticker" in data[0]

def test_by_averages(ingestion):
    response = call.get("/analytics/sectors/averages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "sector" in data[0]

def test_by_earnings(ingestion):
    response = call.get("/analytics/stocks/highest-earnings-growth")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "ticker" in data[0]

def test_by_analyst(ingestion):
    response = call.get("/analytics/stocks/by-analyst-consensus")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "ticker" in data[0]

def test_by_volume(ingestion):
    response = call.get("/analytics/stocks/volume-anomaly")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "ticker" in data[0]
