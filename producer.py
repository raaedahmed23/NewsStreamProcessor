import time
from datetime import datetime
from fetch_news import generateData

from kafka import KafkaProducer
bootstrap_servers=['localhost:9092']
topicName = 'rawdata'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

if __name__ == "__main__":
    for i in range(0, 60):
        data = generateData()
        rrr = bytes(data, 'utf-8')
        print(f'Fetched the data at time : {datetime.now()}')
        ack = producer.send(topicName, rrr)
        conf = ack.get()    
        time.sleep(30)


