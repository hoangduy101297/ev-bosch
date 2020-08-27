import time
import json
import random
from kafka import KafkaProducer

odo_meter = 0

producer = KafkaProducer(bootstrap_servers=['xvc-bosch.westus.cloudapp.azure.com:9092'])
while True:
    speed_limit = input("Enter the speed limit: ")
    battery_status = random.randint(0, 100)
    front_wh_speed = random.randint(0, 50)
    rear_wh_speed = front_wh_speed
    battery_voltage = random.randint(21, 24)
    battery_current = random.randint(0, 10)
    front_break = random.randint(0, 1)
    rear_break = random.randint(0, 1)
    outrigger_detection = random.randint(0, 1)
    core0_load = random.randint(0, 30)
    core1_load = random.randint(0, 30)
    core2_load = random.randint(0, 30)
    odo_meter = odo_meter + 1
    current_milli_time = int(round(time.time() * 1000))
    send_data = {
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
            "error_message": "error1",
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
    print(json.dumps(send_data, indent=2))
    try:
        producer.send('vsk-topic', value=json.dumps(send_data, indent=2))
        time.sleep(5)
    except Exception as ex:
        print(ex)
