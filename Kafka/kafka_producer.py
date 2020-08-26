import time
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['xvc-bosch.westus.cloudapp.azure.com:9092'])
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
        "speed_limit": 100, 
        "battery_status": 10, 
        "front_wh_speed": 22, 
        "rear_wh_speed": 20, 
        "odo_meter": 10, 
        "battery_voltage": 10, 
        "battery_current": 9,
        "error_message": "error1",
        "front_break": 1, 
        "rear_break": 0, 
        "outrigger_detection": 1
      }
    ]
  }
}
print(json.dumps(send_data, indent=2))
try:
    producer.send('vsk-topic', value=send_data)
    time.sleep(5)
    print("success")
except Exception as ex:
    print(ex)
