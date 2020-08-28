import time
import json
import random
import paho.mqtt.client as mqtt
from kafka import KafkaProducer

odo_meter = 0
broker="xvc-bosch.westus.cloudapp.azure.com"
port=1883

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

producer = KafkaProducer(bootstrap_servers=['xvc-bosch.westus.cloudapp.azure.com:9092'])
while True:
    speed_limit = 50
    battery_status = 80
    front_wh_speed = random.randint(0, speed_limit)
    rear_wh_speed = front_wh_speed
    battery_voltage = random.randint(21, 24)
    battery_current = random.randint(0, 10)
    front_break = random.randint(0, 1)
    rear_break = random.randint(0, 1)
    outrigger_detection = random.randint(0, 1)
    core0_load = round(random.uniform(4.0, 5.0),1)
    core1_load = round(random.uniform(24.0, 25.0),1)
    core2_load = round(random.uniform(0.5, 0.7),1)
    odo_meter = odo_meter + 1
    current_milli_time = int(round(time.time() * 1000))
    kafka_send_data = {
        "action": "TEST_DATA",
        "timestamp": "%d" %(current_milli_time),
        "macId": "d037456fab5d",
        "timeZone": "GMT+7:00",
        "dataType": "PI",
        "data": {
          "point": [
          {
            "type": "PI",
            "speed_limit": speed_limit, 
            "battery_status": battery_status, 
            "front_wh_speed": front_wh_speed, 
            "rear_wh_speed": rear_wh_speed, 
            "odo_meter": odo_meter, 
            "battery_voltage": battery_voltage, 
            "battery_current": battery_current,
            "error_message": "no error",
            "front_break": front_break, 
            "rear_break": rear_break, 
            "outrigger_detection": outrigger_detection,
            "core0_load": core0_load,
            "core1_load": core1_load,
            "core2_load": core2_load
          }
        ]
      }
    }
    mobile_send_data = {
        "maxSpeed": speed_limit,
        "batteryPercent": battery_status,
        "frontWheelSpeed": front_wh_speed,
        "rearWheelSpeed": rear_wh_speed,
        "odoMeter": odo_meter,
        "voltage": battery_voltage,
        "ampere": battery_current,
        "frontBrakeStatus": True,
        "rearBrakeStatus": False,
        }
    print("Kafka:\n"+json.dumps(kafka_send_data, indent=2))
    print("Mobile:\n"+json.dumps(mobile_send_data, indent=2))
    try:
        producer.send('vsk-topic', value=json.dumps(kafka_send_data, indent=2))
        time.sleep(1)
    except Exception as ex:
        print(ex)
    try:
        client1= mqtt.Client("control1")
        client1.on_publish = on_publish
        client1.connect(broker,port)
        ret= client1.publish('mobile-topic',json.dumps(mobile_send_data, indent=2))
    except Exception as ex:
        print(ex)