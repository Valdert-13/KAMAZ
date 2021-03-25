import json
import requests
import asyncio
from aiokafka import AIOKafkaConsumer


KAFKA_HOST = '10.0.0.7:9092'
KAFKA_TOPIK = 'united_trucks_telemetry_decoded'


loop = asyncio.get_event_loop()
async def consume():

    consumer = AIOKafkaConsumer(
        KAFKA_TOPIK, loop=loop, bootstrap_servers=KAFKA_HOST)
    await consumer.start()
    try:
        async for msg in consumer:
            j_item = json.loads(msg.value.decode('utf-8'))
            r = requests.get('http://127.0.0.1:8000/add_data', json=j_item)
            print(r)
    finally:
        await consumer.stop()



loop.run_until_complete(consume())
# item = {"altitude":170.0,"can_data":{"engine_speed":1006,"ignition_switch_from_custom_sensor":1},"can_errors":{},"course":0.0,"latitude":59.251155,"longitude":49.120313333333335,"packet_type":"D","protocol_id":"wialon_ips_2.0","satellites":18,"speed":0.0,"time":"2021-03-24T02:46:47","vehicle_id":"8970199200743715073"}
# j_item = json.dumps(item)
# r = requests.get('http://127.0.0.1:8000/add_data', json=item)
# print(r)
# item = Item(**item)
# print(item.dict())