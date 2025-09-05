import csv
import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.models import MandiPrice


CSV_FILE_PATH = os.path.join('data', 'latest_mandi_prices.csv')
MANDI_COORDS_PATH = os.path.join('data', 'mandi_coords.json')


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except Exception as e:
        print(f"Date parsing error for '{date_str}': {e}")
        return None


def update_mandi_prices():
    session: Session = SessionLocal()
    updated_today = 0

    print("Looking for CSV file at:", os.path.abspath(CSV_FILE_PATH))

    if not os.path.exists(CSV_FILE_PATH):
        print(f"CSV file not found: {CSV_FILE_PATH}")
        return

    if not os.path.exists(MANDI_COORDS_PATH):
        print(f"Mandi coordinates file not found: {MANDI_COORDS_PATH}")
        return

    with open(MANDI_COORDS_PATH, 'r', encoding='utf-8') as f:
        mandi_coords = json.load(f)

    with open(CSV_FILE_PATH, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print(f"CSV headers: {reader.fieldnames}")

        for row in reader:
            try:
                mandi_name = row.get('Market', '').strip()
                crop = row.get('Commodity', '').strip().lower()
                price_str = row.get('Modal_x0020_Price', '').replace(',', '').strip()
                date_str = row.get('Arrival_Date', '').strip()
                state = row.get('State', '').strip()

                if not mandi_name or not crop or not date_str or not price_str:
                    print(f"Skipping row due to missing required field(s): {row}")
                    continue

                date = parse_date(date_str)
                if not date:
                    print(f"Skipping row due to invalid date: {row}")
                    continue

                try:
                    price = float(price_str)
                except ValueError:
                    print(f"Skipping row due to invalid price '{price_str}': {row}")
                    continue

                coords = mandi_coords.get(mandi_name)
                if coords:
                    latitude, longitude = coords
                else:
                    latitude, longitude = 0.0, 0.0

            except Exception as e:
                print(f"Skipping row due to error: {e} | Row: {row}")
                continue

            existing = session.query(MandiPrice).filter(
                MandiPrice.mandi_name == mandi_name,
                MandiPrice.crop == crop,
                MandiPrice.date == date
            ).first()

            if existing:
                existing.price_per_quintal = price
                existing.latitude = latitude
                existing.longitude = longitude
                existing.state = state
            else:
                new_record = MandiPrice(
                    mandi_name=mandi_name,
                    crop=crop,
                    price_per_quintal=price,
                    latitude=latitude,
                    longitude=longitude,
                    date=date,
                    state=state
                )
                session.add(new_record)

            updated_today += 1

        session.commit()
        session.close()

    print(f"Updated/added {updated_today} mandi price records")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    update_mandi_prices()
