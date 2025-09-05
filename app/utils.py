from haversine import haversine
from geopy.geocoders import Nominatim

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in kilometers between two lat/lon points."""
    return haversine((lat1, lon1), (lat2, lon2))

def calculate_profitability(mandi_price: float, quantity: float, distance: float, cost_per_km: float):
    """Calculate net profit, profitability percentage, and transport cost."""
    transport_cost = distance * cost_per_km
    total_revenue = mandi_price * quantity
    net_profit = total_revenue - transport_cost
    profitability_pct = (net_profit / total_revenue) * 100 if total_revenue != 0 else 0
    return round(net_profit, 2), round(profitability_pct, 2), round(transport_cost, 2)

def reverse_geocode_state(latitude: float, longitude: float) -> str:
    """Get state name from latitude and longitude using Nominatim."""
    geolocator = Nominatim(user_agent="smart_crop_advisory")
    location = geolocator.reverse((latitude, longitude), language="en", exactly_one=True)
    if location and 'state' in location.raw['address']:
        return location.raw['address']['state']
    return "Unknown"
