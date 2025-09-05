from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import MandiPrice
from app.schemas import MarketPriceRequest, PriceItem, PriceLookupResponse
from app.utils import calculate_distance, calculate_profitability, reverse_geocode_state
from datetime import date
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Crop Advisory Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows calls from any origin; for production, specify frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods including OPTIONS, POST, GET
    allow_headers=["*"],
)

@app.post("/price-lookup", response_model=PriceLookupResponse)
def price_lookup(req: MarketPriceRequest):
    # Prefer manual state; fallback to reverse geocode
    user_state = req.state.strip() if req.state else reverse_geocode_state(req.latitude, req.longitude)
    if not user_state or user_state.lower() == "unknown":
        raise HTTPException(400, "State could not be determined. Please provide 'state' in request.")

    session: Session = SessionLocal()
    mandis: List[MandiPrice] = session.query(MandiPrice).filter(
        MandiPrice.crop.ilike(req.crop.lower()),
        MandiPrice.state.ilike(user_state)
    ).all()
    session.close()

    if not mandis:
        raise HTTPException(404, f"No mandi prices found for crop '{req.crop}' in {user_state}")

    mandis_with_profit = []
    for mandi in mandis:
        dist = calculate_distance(req.latitude, req.longitude, mandi.latitude, mandi.longitude)
        net_profit, profitability_pct, _ = calculate_profitability(
            mandi.price_per_quintal, req.quantity_quintal, dist, req.transport_cost_per_km
        )
        mandis_with_profit.append(PriceItem(
            mandi_name=mandi.mandi_name,
            price_per_quintal=mandi.price_per_quintal,
            distance_km=dist,
            net_profit=net_profit,
            profitability_percent=profitability_pct
        ))

    # Sort by profitability descending, take top 10
    top_10_mandis = sorted(mandis_with_profit, key=lambda x: x.profitability_percent or 0, reverse=True)[:10]

    if not top_10_mandis:
        raise HTTPException(404, f"No profitable mandis found for crop '{req.crop}' in {user_state}")

    nearest = min(top_10_mandis, key=lambda x: x.distance_km)
    highest_profit = max(top_10_mandis, key=lambda x: x.profitability_percent or 0)
    farthest = max(top_10_mandis, key=lambda x: x.distance_km)

    return PriceLookupResponse(
        user_state=user_state,
        nearest_mandi=nearest,
        highest_profit_mandi=highest_profit,
        all_mandis=top_10_mandis
    )

@app.get("/")
def root():
    return {"message": "Smart Crop Advisory backend running"}
@app.get("/ping")
def ping():
    return {"message": "pong"}
