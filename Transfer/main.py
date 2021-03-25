from fastapi import FastAPI
import uvicorn
import orm
from schemas import Item




app = FastAPI()


@app.get('/get_coordinates')
def get_coordinates(vehicle_id: str):
    return orm.get_coordinates(vehicle_id)

@app.get('/add_data')
async def add_data(msg: Item):
    orm.update(msg)




if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)