from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel


class Item(BaseModel):
    vehicle_id: str
    time: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None
    can_data: Optional[Dict] = None