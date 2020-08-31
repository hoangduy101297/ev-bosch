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
#Timerate to publish MQTT and Kafka
COM_PUBLISH_RATE = 0.5 #500ms

#Time delay to publish COM after reset
RESET_DELAY_TIME = 3 #3s

#Kafka constant
KAFKA_HOST = "xvc-bosch.westus.cloudapp.azure.com"
KAFKA_PORT = 9092

#Mqtt constant
MQTT_HOST = "xvc-bosch.westus.cloudapp.azure.com"
MQTT_PORT = 1883

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
    global global_data
    
    while True:
        rcv_msg = canBus.recv(timeout = None)
        
        CAN_src = getCanSource(rcv_msg.arbitration_id)
        
        if CAN_src != 0:
            setGlobalLock()
            updateDataFromCan(CAN_src, rcv_msg.data)
            resetGlobalLock()
        
        
#Publish Kafka and MQTT
def COM_Publish_Thread():
	time.sleep(RESET_DELAY_TIME)
    while True:

        print("Kafka:\n"+json.dumps(kafka_send_data, indent=2))
        print("Mobile:\n"+json.dumps(mobile_send_data, indent=2))
        try:
            kafkaProducer.send('vsk-topic', value=json.dumps(kafka_send_data, indent=2))
            time.sleep(1)
        except Exception as ex:
            print(ex)
        try:
            client1= mqtt.Client("control1")
            client1.on_publish = on_publish
            client1.connect(MQTT_HOST,MQTT_PORT)
            ret= client1.publish('mobile-topic',json.dumps(mobile_send_data, indent=2))
        except Exception as ex:
            print(ex)
        time.sleep(1)


#Listen MQTT message from Mobile, for Setting speed limit
def MQTT_Listen_Thread():
    while True:
        print("MQTT_thread")
        time.sleep(1)



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
	while getGlobalLock():
		pass
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

#######################################################################
#Def publish Kafka and MQTT func
#######################################################################

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass




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
    global COM_Publish, MQTT_Listen, canBus, kafkaProducer
    
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
