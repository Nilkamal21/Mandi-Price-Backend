from pydantic import BaseModel, PositiveFloat
from typing import List, Optional
from enum import Enum

class LanguageEnum(str, Enum):
    english = "en"
    hindi = "hi"
    punjabi = "pa"
    bengali = "bn"


class MarketPriceRequest(BaseModel):
    crop: str
    latitude: float
    longitude: float
    quantity_quintal: PositiveFloat
    transport_cost_per_km: float
    state: Optional[str] = None  # Optional manual state input

class PriceItem(BaseModel):
    mandi_name: str
    price_per_quintal: float
    distance_km: float
    net_profit: Optional[float] = None
    profitability_percent: Optional[float] = None

class PriceLookupResponse(BaseModel):
    user_state: str
    nearest_mandi: PriceItem
    highest_profit_mandi: PriceItem
    all_mandis: List[PriceItem]
