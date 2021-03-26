from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel


class Can_Data(BaseModel):
    accelerator_pedal_position_1: Optional[int]
    cargo_weight: Optional[int]
    engine_speed: Optional[int]
    tachograph_vehicle_speed: Optional[int]
    fuel_level_1: Optional[int]
    high_resolution_engine_total_fuel_used: Optional[float]
    high_resolution_engine_trip_fuel: Optional[float]
    high_resolution_total_vehicle_distance: Optional[int]
    high_resolution_trip_distance: Optional[float]
    wheel_based_vehicle_speed: Optional[int]
    service_brake_circuit_1_air_pressure: Optional[float]
    service_brake_circuit_2_air_pressure: Optional[float]
    engine_fuel_temperature_1: Optional[int]
    engine_oil_pressure: Optional[int]


class Item(BaseModel):
    vehicle_id: str
    time: Optional[datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: Optional[float]
    speed: Optional[float]
    can_data: Optional[Can_Data]
    course: Optional[float]
    can_errors: Optional[Dict]

