# Stock Data Pipeline

A stock analytics API built with FastAPI, PostgreSQL, Redis, and Docker; deployed on AWS.

**Live API:** http://3.135.1.12:8000/docs

---

## Overview

Ingests daily stock data for 50 S&P 500 tickers across 5 sectors using yfinance. Includes 7 analytics endpoints with Redis caching on the heaviest queries. Deployed on AWS with automated daily data refresh using EventBridge.

---

## Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Redis**
- **Docker**
- **AWS ECS Fargate**
- **AWS EventBridge**
- **CI/CD**
