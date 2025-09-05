from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base
import datetime

class MandiPrice(Base):
    __tablename__ = "mandi_prices"
    id = Column(Integer, primary_key=True, index=True)
    mandi_name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    state = Column(String, index=True, nullable=False)
    crop = Column(String, index=True, nullable=False)
    price_per_quintal = Column(Float, nullable=False)
    date = Column(Date, default=datetime.date.today, nullable=False)
