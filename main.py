#######################################################################
#Import Packages
#######################################################################
import time
import can
import sys
import json
import kafka
from threading import Thread


#######################################################################
#Define Global constant
#######################################################################
#Timerate to publish MQTT and Kafka
COM_PUBLISH_RATE = 0.5 #500ms

#Assign main thread and side threads
MAIN_THREAD = CAN_Thread
THREAD_1 = COM_Publish_Thread
THREAD_2 = MQTT_Listen_Thread

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
thread1 = None
thread2 = None

canBus = None

kafkaProducer = None
mqttClient = None

#######################################################################
#######################################################################

#######################################################################
#Define Threads
#RPi 3 can run up to 4 threads
#######################################################################
def CAN_Thread():
#Read and proceed CAN data
    pass

def COM_Publish_Thread():
#Publish Kafka and MQTT
    time.sleep(COM_PUBLISH_RATE)

def MQTT_Listen_Thread():
#Listen MQTT message from Mobile, for Setting speed limit
    pass


#######################################################################
#Define Main Thread, just assign above thread into main thread
#######################################################################
def main_Thread():
	if MAIN_THREAD == CAN_Thread:
		while True:
			CAN_Thread()
	elif MAIN_THREAD == COM_Publish_Thread:
		while True:
			COM_Publish_Thread()
	else: 
		while True:
			MQTT_Listen_Thread()



#######################################################################
#Define Internal functions
#######################################################################
def init():
#Set up all objects
    global thread1, thread2, canBus, kafkaProducer
    
    #Init side Threads
    thread1 = Thread(target = THREAD_1)
    thread2 = Thread(target = THREAD_2)
    
    CAN.setDaemon(True)
    COM_Publish.setDaemon(True)
    MQTT_Listen.setDaemon(True)

    #Init CAN bus
    canBus = can.interface.Bus(bustype='socketcan', channel=CAN_CHANNEL ,bitrate=CAN_BITRATE)

    #Init Kafka
    kafkaProducer = KafkaProducer(bootstrap_servers=[KAFKA_HOST+":"+str(KAFKA_PORT)])
    
    #Init MQTT


def init_End():
#Start all processes
	global thread1, thread2

	#Start side Threads
	thread1.start()
	thread2.start()


if __name__ == "__main__":
	#Initialize stuff
	init()
	init_End()

	#Main Thread
	main_Thread()
	sys.exit()
