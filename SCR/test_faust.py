import faust

KAFKA_HOST = '10.0.0.7:9092'
KAFKA_TOPIK = 'united_trucks_telemetry_decoded'

app = faust.App('united_trucks_telemetry_decoded', broker='kafka://10.0.0.7:9092', fetch_max_bytes = 1_024)

class Order(faust.Record):
    time: str
    speed: float

@app.agent(value_type=Order)
async def order(orders):
    async for order in orders:
        print(f'speed = {order.speed}')

if __name__ == '__main__':
    app.main()