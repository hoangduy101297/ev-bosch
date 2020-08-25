import time

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

producer.send('demo-topic', value='456')
time.sleep(0.01)
