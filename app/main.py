from fastapi import FastAPI
from app.routers.analytics import router_analytics
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router_analytics)
