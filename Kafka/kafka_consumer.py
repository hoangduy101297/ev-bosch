from kafka import KafkaConsumer
consumer = KafkaConsumer('demo-topic', bootstrap_servers=['localhost:9092'])
for message in consumer:
    print (message)