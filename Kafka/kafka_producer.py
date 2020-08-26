import time

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['xvc-bosch.westus.cloudapp.azure.com:9092'])

try:
    producer.send('vsk-topic', value='testtttttttttt')
    time.sleep(0.1)
except Exception as ex:
    print(ex)
