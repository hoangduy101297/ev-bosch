#######################################################################
#Import Packages
#######################################################################
import time
#import can
import sys
import json
import kafka
import my_can_lib
from threading import Thread


#######################################################################
#Define Global configuration
#######################################################################
#Timerate to publish MQTT and Kafka
COM_PUBLISH_RATE = 0.5 #500ms

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


#######################################################################
#Declare Global Var
#######################################################################
global_data = {
    'FR_SPD': 0,
    'RR_SPD': 0,
    'BRK': 0,
    'APP': 0,
    'UBAT': 0,
    'ERR': 'No error'
}

global_lock = {
    'VCU1': 0,
    'VCU2': 0,
    'INVERTER': 0,
    'ABS': 0,
    'PI': 0,
    'RADAR': 0,
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
            setLock(CAN_src)
            my_can_lib.UpdateDataFromCan(global_data, CAN_src, rcv_msg.data)
            resetLock(CAN_src)
        
        
#Publish Kafka and MQTT
def COM_Publish_Thread():
    while True:
        print("COM_thread")
        time.sleep(COM_PUBLISH_RATE)


#Listen MQTT message from Mobile, for Setting speed limit
def MQTT_Listen_Thread():
    while True:
        print("MQTT_thread")
        time.sleep(1)


#######################################################################
#Define Main Thread, just assign above thread into main thread
#######################################################################
def main_Thread():
    CAN_Thread()

#######################################################################
#Define Internal functions
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


#Start all processes
def init_End():
    global COM_Publish, MQTT_Listen

    #Start side Threads
    COM_Publish.start()
    MQTT_Listen.start()


#Set and reset global lock for data consistency
def setLock(lockName):
    global global_lock
    global_lock[lockName] = 1
    
def resetLock(lockName):
    global global_lock
    global_lock[lockName] = 0    

#get status of global Lock 
def getLock(lockName):
    return global_lock[lockName]


#Return Key of the val in a dictionary
def getCanSource(val):
    for key, value in CAN_ID.items():
        if val == value:
            return key
    return 0

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
