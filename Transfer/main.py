import kafka
import json
from schemas import Item
from orm import update

KAFKA_HOST = 
KAFKA_TOPIK = 

consumer = kafka.KafkaConsumer(KAFKA_TOPIK,
                               bootstrap_servers=[KAFKA_HOST],
                               fetch_max_bytes = 1_024)

for message in consumer:
    try:
        j_item = json.loads(message.value.decode('utf-8'))
        item = Item(**j_item)
        update(item, j_item)
        #print(f'Get {item.vehicle_id}')
    except:
        
        pass


