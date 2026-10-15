import json
import os
import math
from typing import List, Optional, Dict, Any
from .schemas import FacilityItem, FacilityListResponse

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sample_facilities.json")

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points on the Earth in kilometers."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

class FacilityService:
    def __init__(self):
        self.facilities: List[Dict[str, Any]] = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.facilities = json.load(f)
        else:
            self.facilities = []

    def get_facilities(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        emergency_only: bool = False,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance_km: Optional[float] = None
    ) -> FacilityListResponse:
        results = []
        q = (query or "").strip().lower()
        cat = (category or "").strip().upper()

        for fac in self.facilities:
            # Emergency filter
            if emergency_only and not fac.get("is_24x7_emergency", False):
                continue

            # Category filter
            if cat and cat != "ALL":
                if fac.get("category", "").upper() != cat:
                    continue

            # Text query filter across multiple fields
            if q:
                searchable = " ".join([
                    fac.get("name", ""),
                    fac.get("type", ""),
                    fac.get("village_town", ""),
                    fac.get("district", ""),
                    fac.get("pincode", ""),
                    fac.get("address", ""),
                    " ".join(fac.get("services", []))
                ]).lower()
                if q not in searchable:
                    continue

            # Distance calculation if coordinates are provided
            distance_val = None
            if lat is not None and lon is not None:
                try:
                    f_lat = float(fac["latitude"])
                    f_lon = float(fac["longitude"])
                    distance_val = haversine_distance(lat, lon, f_lat, f_lon)
                    if max_distance_km and distance_val > max_distance_km:
                        continue
                except (ValueError, KeyError):
                    pass

            item = FacilityItem(
                id=fac["id"],
                name=fac["name"],
                type=fac["type"],
                category=fac["category"],
                address=fac["address"],
                village_town=fac["village_town"],
                district=fac["district"],
                pincode=fac["pincode"],
                latitude=fac["latitude"],
                longitude=fac["longitude"],
                phone=fac["phone"],
                emergency_phone=fac["emergency_phone"],
                is_24x7_emergency=fac["is_24x7_emergency"],
                services=fac["services"],
                doctor_availability=fac["doctor_availability"],
                transport_info=fac["transport_info"],
                is_demo_data=fac["is_demo_data"],
                verified_label=fac["verified_label"],
                distance_km=distance_val
            )
            results.append(item)

        # Sort by distance if user coordinates provided, otherwise alphabetical
        if lat is not None and lon is not None:
            results.sort(key=lambda x: x.distance_km if x.distance_km is not None else 99999)
        else:
            # Sort emergency facilities first, then name
            results.sort(key=lambda x: (not x.is_24x7_emergency, x.name))

        loc_dict = {"latitude": lat, "longitude": lon} if (lat is not None and lon is not None) else None

        return FacilityListResponse(
            total=len(results),
            facilities=results,
            query_used=query,
            applied_category=category,
            user_location=loc_dict
        )

    def get_facility_by_id(self, facility_id: str) -> Optional[FacilityItem]:
        for fac in self.facilities:
            if fac["id"] == facility_id:
                return FacilityItem(
                    id=fac["id"],
                    name=fac["name"],
                    type=fac["type"],
                    category=fac["category"],
                    address=fac["address"],
                    village_town=fac["village_town"],
                    district=fac["district"],
                    pincode=fac["pincode"],
                    latitude=fac["latitude"],
                    longitude=fac["longitude"],
                    phone=fac["phone"],
                    emergency_phone=fac["emergency_phone"],
                    is_24x7_emergency=fac["is_24x7_emergency"],
                    services=fac["services"],
                    doctor_availability=fac["doctor_availability"],
                    transport_info=fac["transport_info"],
                    is_demo_data=fac["is_demo_data"],
                    verified_label=fac["verified_label"]
                )
        return None

facility_service = FacilityService()
