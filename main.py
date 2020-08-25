#######################################################################
#Import Packages
#######################################################################
import time
#import can
import sys
import json
import kafka
from threading import Thread


#######################################################################
#Define Global constant
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

#######################################################################
#Declare Global Obj/ Var
#######################################################################
COM_Publish = None
MQTT_Listen = None

canBus = None

kafkaProducer = None
mqttClient = None

#######################################################################
#######################################################################

#######################################################################
#Define Threads
#RPi 3 can run up to 4 threads
#######################################################################

#Read and proceed CAN data
def CAN_Thread():
    while True:
        print("CAN_thread")
        time.sleep(0.1)
        
        
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
def init():
#Set up all objects
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


def init_End():
#Start all processes
	global COM_Publish, MQTT_Listen

	#Start side Threads
	COM_Publish.start()
	MQTT_Listen.start()


if __name__ == "__main__":
	#Initialize stuff
	init()
	init_End()

	#Main Thread
	main_Thread()
	sys.exit()
