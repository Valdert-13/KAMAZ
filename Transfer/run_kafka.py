import json
import requests
import asyncio
from aiokafka import AIOKafkaConsumer


KAFKA_HOST = '10.0.0.7:9092'
KAFKA_TOPIK = 'united_trucks_telemetry_decoded'


loop = asyncio.get_event_loop()
async def initialize():

    consumer = AIOKafkaConsumer(
        KAFKA_TOPIK, loop=loop, bootstrap_servers=KAFKA_HOST)
    await consumer.start()
    try:
        async for msg in consumer:
            j_item = json.loads(msg.value.decode('utf-8'))
            requests.get('http://127.0.0.1:8000/add_data', json=j_item)
    finally:
        await consumer.stop()



loop.run_until_complete(initialize())
