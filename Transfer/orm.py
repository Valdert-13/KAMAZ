from pony.orm import *
from datetime import datetime, timedelta

db = Database()

class Unit(db.Entity):
    vehicle_id = PrimaryKey(str)
    time = Optional(datetime)
    latitude = Optional(float)
    longitude = Optional(float)
    # altitude = Optional(float)
    # speed = Optional(float)
    info = Optional(Json, default={})


db.bind('sqlite', 'database.sqlite',  create_db=True) # Заменить данные на подключение PostgreSQL

db.generate_mapping(create_tables=True)

@db_session(serializable = True )
def update(item, info):
    """Добовление и обновленние данных в базу данных
    Parameters
    ----------
     item: pydantic.BaseModel
        Экземпляр класса BaseModel
    info: Json
        Json - c первоночальными данными"""
    vehicle_id = item.vehicle_id
    if Unit.exists(vehicle_id=vehicle_id):
        if Unit[vehicle_id].time < item.time:
            if item.time:
                Unit[vehicle_id].time = item.time
            if item.latitude:
                Unit[vehicle_id].latitude = item.latitude
            if item.longitude:
                Unit[vehicle_id].longitude = item.longitude
            # if item.altitude:
            #     Unit[vehicle_id].altitude = item.altitude
            # if item.speed:
            #     Unit[vehicle_id].speed = item.speed
            if info:
                Unit[vehicle_id].info = info
    else:
        Unit(vehicle_id = item.vehicle_id,
             time = datetime.today() - timedelta(days=4))





