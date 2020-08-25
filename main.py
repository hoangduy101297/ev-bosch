################
#Import Packages
################
import time
import can
from threading import Thread


#########################
#Declare Global Obj/ Var
#########################
CAN = None
COM_Publish = None
MQTT_Listen = None

canBus = None

#######################
#Define Global constant
#######################
COM_PUBLISH_RATE = 0.5 #500ms
kafka_host = "xvc-bosch.westus.cloudapp.azure.com"
kafka_port = "9092"



###############
#Define Threads
###############
#RPi 3 can run up to 4 threads


def CAN_Thread():
#Read and proceed CAN data
    pass

def COM_Publish_Thread():
#Publish Kafka and MQTT
    time.sleep(COM_PUBLISH_RATE)

def MQTT_Listen_Thread():
#Listen MQTT message from Mobile, for Setting speed limit
    pass





##########################
#Define Internal functions
##########################
def init():
    global canBus, CAN, COM, MQTT
    
    #Init Threads
    CAN = Thread(target = CAN_Thread)
    COM_Publish = Thread(target = COM_Publish_Thread)
    MQTT_Listen = Thread(target = MQTT_Listen_Thread)
    
    CAN.setDaemon(True)
    COM_Publish.setDaemon(True)
    MQTT_Listen.setDaemon(True)


    #Init CAN bus
    canBus = can.interface.Bus(bustype='socketcan', channel = 'can0',bitrate=500000)

    #Init Kafka
    
    
    #Init MQTT

###################
#Define Main Thread
###################
def main_Thread():
    
    while True:
        pass



if __name__ == "__main__":
    init()
    #Start Threads
    main_Thread()
