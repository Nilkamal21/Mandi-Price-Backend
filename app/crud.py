from sqlalchemy.orm import Session
from .models import MandiPrice
from datetime import date

def get_cached_prices(session: Session, crop: str):
    return session.query(MandiPrice).filter(
        MandiPrice.crop.ilike(crop),
        
    ).all()
