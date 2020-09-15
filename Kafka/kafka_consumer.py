from kafka import KafkaConsumer
consumer = KafkaConsumer('vsk-topic', bootstrap_servers=['xvc-bosch.westus.cloudapp.azure.com:9092'])
for message in consumer:
    print (message)