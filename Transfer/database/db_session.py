from pony.orm import *
from datetime import datetime, timedelta
from .model import Unit
import json

@db_session(serializable = True )
def update(item):
    """Добовление и обновленние данных в базу данных
    Parameters
    ----------
     item: pydantic.BaseModel
        Экземпляр класса BaseModel
    info: Json
        Json - c первоночальными данными"""
    vehicle_id = item.vehicle_id
    if Unit.exists(vehicle_id=vehicle_id):
        try:
            if Unit[vehicle_id].time < item.time and item.time is not None:
                Unit[vehicle_id].time = item.time
                Unit[vehicle_id].info = json.loads(item.json())
                if item.latitude:
                    Unit[vehicle_id].latitude = item.latitude
                if item.longitude:
                    Unit[vehicle_id].longitude = item.longitude
        except TypeError:
            pass
    else:
        Unit(vehicle_id = item.vehicle_id,
             time = datetime.today() - timedelta(days=4))




@db_session()
def get_coordinates(vehicle_id: str):
    """Запрос на координаты"""
    if Unit.exists(vehicle_id=vehicle_id):
        return {'latitude':Unit[vehicle_id].latitude,
                'longitude': Unit[vehicle_id].longitude}
    else:
        return {'latitude':None,
                'longitude': None}

