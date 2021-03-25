from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel


class Can_Data(BaseModel):
    accelerator_pedal_position_1: Optional[int] = None
    cargo_weight: Optional[int] = None
    engine_speed: Optional[int] = None
    high_resolution_engine_total_fuel_used: Optional[float] = None
    high_resolution_engine_trip_fuel: Optional[float] = None
    high_resolution_total_vehicle_distance: Optional[int] = None
    high_resolution_trip_distance: Optional[float] = None
    wheel_based_vehicle_speed: Optional[int] = None


class Item(BaseModel):
    vehicle_id: str
    time: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None
    can_data: Optional[Can_Data] = None
    course: Optional[float] = None
    can_errors: Optional[Dict] = None

    class Config:
        orm_mode = True