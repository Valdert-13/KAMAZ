from pony.orm import *
from datetime import datetime

db = Database()

class Unit(db.Entity):
    _table_ = "current_state_vehicle"
    vehicle_id = PrimaryKey(str)
    time = Optional(datetime)
    latitude = Optional(float)
    longitude = Optional(float)
    info = Optional(Json, default={})

db.bind('sqlite', './../database.sqlite',  create_db=True) # Заменить данные на подключение PostgreSQL

db.generate_mapping(create_tables=True)