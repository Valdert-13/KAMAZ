from fastapi import FastAPI
import uvicorn
from database import db_session
from database.schemas import Item
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
fh = logging.FileHandler('logging.log')
fh.setLevel(logging.DEBUG)
log.addHandler(fh)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    log.info('Initializing API ...')


@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')


@app.get('/get_coordinates')
async def get_coordinates(vehicle_id: str):
    return db_session.get_coordinates(vehicle_id)


@app.post('/add_data')
async def add_data(msg: Item):
    db_session.update(msg)




if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
