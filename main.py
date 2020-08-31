#######################################################################
#Import Packages
#######################################################################
import time
#import can
import sys
import json
import kafka
from threading import Thread
import random #used for testing, remove in final version
import paho.mqtt.client as mqtt
from kafka import KafkaProducer

######################################################################
#																	 #
#					  	   Configuration 					         #
#																	 #
######################################################################
#Timerate to publish MQTT and Kafka. MIN 1s
COM_PUBLISH_RATE = 1 #1s

#Time delay to publish COM after reset
RESET_DELAY_TIME = 3 #3s

#Kafka constant
KAFKA_HOST = "xvc-bosch.westus.cloudapp.azure.com"
KAFKA_PORT = 9092
KAFKA_MACID = "d037456fab5d"
KAFKA_SEND_TOPIC = "vsk-topic"

#Mqtt constant
MQTT_HOST = "xvc-bosch.westus.cloudapp.azure.com"
MQTT_PORT = 1883
MQTT_SEND_TOPIC = "mobile-topic"
MQTT_RECV_TOPIC = "TBD"


#CAN constant
CAN_BITRATE = 500000
CAN_CHANNEL = 'can0'

CAN_ID = {
    'VCU1': 18,
    'VCU2': 19,
    'INVERTER': 21,
    'ABS': 100,
    'PI': 101,
    'RADAR': 102, 
}

#Data position in CAN frame
CAN_pos = {
    'VCU1':{
        'spd':0,
        'brk':1
    },
    
    'VCU2':{
        'ubat':0,
        'app':1
    },
    
    'INVERTER':{
    },
    
    'ABS':{
    },
    
    'PI':{
    },
    
    'RADAR':{
    }
}


######################################################################
#																	 #
#					  	   Implementation 					         #
#																	 #
######################################################################

#######################################################################
#Declare Global Var
#######################################################################
global_lock = 0
global_data = {
    "speed_limit": 0, 
    "battery_status": 0, 
    "front_wh_speed": 0, 
    "rear_wh_speed": 0, 
    "odo_meter": 0, 
    "battery_voltage": 0, 
    "battery_current": 0,
    "error_message": "no error",
    "front_break": 0, 
    "rear_break": 0, 
    "outrigger_detection": 0,
    "core0_load": 0,
    "core1_load": 0,
    "core2_load": 0,
}


#######################################################################
#Declare Global Obj
#######################################################################
COM_Publish = None
MQTT_Listen = None

canBus = None

kafkaProducer = None
mqttClient = None


#######################################################################
#Define Threads
#RPi 3 can run up to 4 threads
#######################################################################

#Read and proceed CAN data
def CAN_Thread():
    while True:
        rcv_msg = canBus.recv(timeout = None)
        
        CAN_src = getCanSource(rcv_msg.arbitration_id)
        
        if CAN_src != 0:
            setGlobalLock()
            updateDataFromCan(CAN_src, rcv_msg.data)
            resetGlobalLock()
        
        
#Publish Kafka and MQTT
def COM_Publish_Thread():
	global mqttClient, kafkaProducer

	#After start-up, we should wait some times before starting sending Kafka and MQTT
	time.sleep(RESET_DELAY_TIME)

    while True:
    	kafka_send_data, mobile_send_data = updatePayload()

        try:
            mqttClient.publish(MQTT_SEND_TOPIC,json.dumps(mobile_send_data, indent=2))
        except:
            pass

        try:
            kafkaProducer.send(KAFKA_SEND_TOPIC, value=json.dumps(kafka_send_data, indent=2))
        except:
            pass

        time.sleep(COM_PUBLISH_RATE)


#Listen MQTT message from Mobile, for Setting speed limit
def MQTT_Listen_Thread():
	global mqttClient
    mqttClient.loop_forever()



#######################################################################
#Define useful API
#######################################################################

#Set and reset global lock for data consistency
# 1: Lock is active
# 0: Lock is inactive
def setGlobalLock():
    global global_lock
    global_lock = 1
    
def resetGlobalLock():
    global global_lock
    global_lock = 0    

#get status of global Lock 
# 1: Lock is active
# 0: Lock is inactive
def getGlobalLock():
    return global_lock


#Return Key of the val in a dictionary
def getCanSource(val):
    for key, value in CAN_ID.items():
        if val == value:
            return key
    return 0

#Update CAN data to global_data
def updateDataFromCan(src, data):
	global global_data
    for x in CAN_pos[src]:
        global_data[x] = data[CAN_pos[src][x]]

#Update data from global_data to Kafka and MQTT payload
def updatePayload():
	#Currently not implement the Global Lock, data may be inconsistent in some case
	#while getGlobalLock():
		#pass
   	current_milli_time = int(round(time.time() * 1000))
    kafka_data = {
        "action": "TEST_DATA",
        "timestamp": "%d" %(current_milli_time),
        "macId": KAFKA_MACID,
        "timeZone": "GMT+7:00",
        "dataType": "PI",
        "data": {
          "point": [
          {
            "type": "PI",
            "speed_limit": global_data["speed_limit"], 
            "battery_status": global_data["battery_status"], 
            "front_wh_speed": global_data["front_wh_speed"], 
            "rear_wh_speed": global_data["rear_wh_speed"], 
            "odo_meter": global_data["odo_meter"], 
            "battery_voltage": global_data["battery_voltage"], 
            "battery_current": global_data["battery_current"],
            "error_message": global_data["error_message"],
            "front_break": global_data["front_break"], 
            "rear_break": global_data["rear_break"], 
            "outrigger_detection": global_data["outrigger_detection"],
            "core0_load": global_data["core0_load"],
            "core1_load": global_data["core1_load"],
            "core2_load": global_data["core2_load"]
          }
        ]
      }
    }
    mobile_data = {
        "maxSpeed": global_data["speed_limit"],
        "batteryPercent": global_data["battery_status"],
        "frontWheelSpeed": global_data["front_wh_speed"],
        "rearWheelSpeed": global_data["rear_wh_speed"],
        "odoMeter": global_data["odo_meter"],
        "voltage": global_data["battery_voltage"],
        "ampere": global_data["battery_current"],
        "frontBrakeStatus": True if global_data["front_break"] == 1 else False,
        "rearBrakeStatus": True if global_data["rear_break"] == 1 else False,
        }

    return kafka_data, mobile_data

#######################################################################
#MQTT & Kafka callbacks
#######################################################################

def mqtt_on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, rc):
    global mqttClient

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqttClient.subscribe("mobile-topic")

######################################################################
#																	 #
#					  Hardcode, do not change!!!  					 #
#																	 #
######################################################################

#######################################################################
#Define Init/Ini func
#######################################################################
#Set up all objects
def init():
    global COM_Publish, MQTT_Listen, canBus, kafkaProducer, mqttClient
    
    #Init side Threads
    COM_Publish = Thread(target = COM_Publish_Thread)
    MQTT_Listen = Thread(target = MQTT_Listen_Thread)
    
    COM_Publish.setDaemon(True)
    MQTT_Listen.setDaemon(True)

    #Init CAN bus
    canBus = can.interface.Bus(bustype='socketcan', channel=CAN_CHANNEL ,bitrate=CAN_BITRATE)

    #Init Kafka
    kafkaProducer = KafkaProducer(bootstrap_servers=[KAFKA_HOST+":"+str(KAFKA_PORT)])
    
    #Init MQTT
    mqttClient= mqtt.Client("control1")
    mqttClient.on_message = mqtt_on_message
    mqttClient.on_connect = mqtt_on_connect
    mqttClient.connect(MQTT_HOST,MQTT_PORT)

#Start all processess
def init_End():
    global COM_Publish, MQTT_Listen

    #Start side Threads
    COM_Publish.start()
    MQTT_Listen.start()


#######################################################################
#Define Main Thread, just assign above thread into main thread
#######################################################################
def main_Thread():
    CAN_Thread()


#######################################################################
#Main Program Flow
#######################################################################
if __name__ == "__main__":
	#Initialize stuff
	init()
	init_End()

	#Main Thread
	main_Thread()
	sys.exit()
