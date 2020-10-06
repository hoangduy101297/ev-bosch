#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
#Import Packages
#######################################################################
from __future__ import division
import time
import can
import sys
import json
import kafka
import psutil
from threading import Thread
import random #used for testing, remove in final version
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from my_can_lib import *
import subprocess


######################################################################
#																	 #
#					  	   Configuration 					         #
#																	 #
######################################################################
#Debug conf (=1 debug message print out)
debug_msg = 1

#global variables for Init()
initDone_kafka = 0
initDone_MQTT = 0
retry_time = 5
retry_cnt = 0

#Timerate to publish MQTT and Kafka. MIN 1s
COM_PUBLISH_RATE = 1 #700ms

#Time delay to publish COM after reset
RESET_DELAY_TIME = 1 #1s

#Kafka constant
KAFKA_HOST = "xvc-bosch.westus.cloudapp.azure.com"
KAFKA_PORT = 9092
KAFKA_MACID = "d037456fab5d"
KAFKA_SEND_TOPIC = "vsk-topic"

#Mqtt constant
MQTT_HOST = "xvc-bosch.westus.cloudapp.azure.com"
MQTT_PORT = 1883
MQTT_SEND_TOPIC = "mobile-topic"
MQTT_RECV_TOPIC = "mobileToPi-topic"

#Error array
errorArr = [0,          0,             0,          0]
#           ^           ^              ^           ^
#   MQTT_conn_err MQTT_publish_err CAN_recei_err speedLimit_deny

#CAN constant
CAN_BITRATE = 500000
CAN_CHANNEL = 'can0'

CAN = {
    'VCU1':{
        'id':21,
        'func': updateDataVCU1
     },
    'VCU2':{
        'id':22,
        'func': updateDataVCU2
     },
    'IVT1':{
        'id':35,
        'func': updateDataIVT1
     },
    'IVT2':{
        'id':36,
        'func': updateDataIVT2
     },
    'CoreLoad0':{
        'id':24,
        'func': updateDataCoreLoad0
     },
    'CoreLoad1':{
        'id':25,
        'func': updateDataCoreload1
     },
    'CoreLoad2':{
        'id':26,
        'func': updateDataCoreLoad2
     },
    'ABS':{
        'id':16,
        'func': updateDataABS
     },
    'PI1':{
        'id':18,
        'func': updateDataPI1
     },
    'PI2':{
        'id':42,
        'func': updateDataPI2
     },
    'RADAR':{
        'id':103,
        'func': updateDataRADAR
     }
}
global TRAF_ID_MOBILE
TRAF_ID_MOBILE = {
    "NoTraf":0,
    "NoLim":1,
    "Pedes":2,
    "SpdLim":3,
    "Stop":4
}
global TRAF_ID_VCU
TRAF_ID_VCU = {
    "NoLim":0,
    "Pedes":1,
    "SpdLim":2,
    "Stop":3,
    "NoTraf":4
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
    "trafficSign": "NoTraf",
    "msgSrc": "VSK",
    "newTrafSign_flg": 0,
    "speed_limit_traf":0,
    "t15_st":0
}

#######################################################################
#Declare Global Obj
#######################################################################
COM_Publish = None
MQTT_Listen = None
TrafSign = None
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
        try:
            rcv_msg = canBus.recv(timeout = None)
##            CAN_err = 0 if rcv_msg.find('ID: 0004') == -1 else 1
##            print(rcv_msg)
            updateDataFromCan(rcv_msg)
            
##            if CAN_err == 1:
##                reportErr("CAN_recei_err")
##            else:
##                clearErrReport("CAN_recei_err")
##            print(rcv_msg)
        except:
            pass
        
        
#Publish Kafka and MQTT
def COM_Publish_Thread():
    global mqttClient, kafkaProducer,debug_msg,initDone_MQTT,initDone_kafka

    #After start-up, we should wait some times before starting sending Kafka and MQTT
    time.sleep(RESET_DELAY_TIME)

    #Reset Speed limit to 0, send to VSK/Mobile
    mqtt_msg = {
            "maxSpeed": 0
        }
    try:
        mqttClient.publish(MQTT_RECV_TOPIC,json.dumps(mqtt_msg, indent=2), retain = True)
    except:
        pass

    while True:
        kafka_send_data, mobile_send_data = updatePayload()

        if initDone_MQTT == 1:
            try:
                mqttClient.publish(MQTT_SEND_TOPIC,json.dumps(mobile_send_data, indent=2))
                clearErrReport("MQTT_publish_err")
            except Exception as ex:
                reportErr("MQTT_publish_err")
                if(debug_msg == 1):
                    print("Can't publish message MQTT: ", ex)

        if initDone_kafka == 1:
            try:
                kafkaProducer.send(KAFKA_SEND_TOPIC, value=json.dumps(kafka_send_data, indent=2))
            except Exception as ex:
                if(debug_msg == 1):
                    print("Can't publish message kafka: ", ex)
        if(debug_msg == 1):
            print(global_data)    
        time.sleep(COM_PUBLISH_RATE)


#Listen MQTT message from Mobile, for Setting speed limit
def MQTT_Listen_Thread():
    global mqttClient
    mqttClient.loop_forever()

def TrafSign_Thread():
    global global_data, canBus

    while True:
        #if global_data["newTrafSign_flg"]:
        data = [TRAF_ID_VCU[global_data["trafficSign"]],global_data["speed_limit_traf"],0,0,int(global_data["speed_limit"]*2),0,0,0]
        message = can.Message(arbitration_id=CAN['PI1']['id'], extended_id=False, data=data)
        try:
            canBus.send(message)
        except Exception as ex:
            pass
        time.sleep(0.1)
        #else:
            #pass


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
        if val == value['id']:
            return key
    return 0

#Update CAN data to global_data
def updateDataFromCan(msg):
    global global_data
    for key, can_properties in CAN.items():
        if msg.arbitration_id == can_properties['id']:
##            try:
                can_properties['func'](msg.data, global_data)
                break
##            except:
##                reportErr("CAN_recei_err")
##                pass
        
def updateErrMsg():
    global errorArr,global_data,debug_msg
    global_data["error_message"] = ''
    if errorArr[0] == 1:
        global_data["error_message"] += "MQTT connection error \n"
        
    if errorArr[1] == 1:
        global_data["error_message"] += "MQTT publish error \n"
        
    if errorArr[2] == 1:
        global_data["error_message"] += "CAN package receive error \n"
        
    if errorArr[3] == 1:
        global_data["error_message"] += "Speed limit is now control by mobile app \n"
        
    if global_data["error_message"] == '':
        global_data["error_message"] = "no error"
        
def reportErr(error):
    global errorArr,debug_msg
    if error == "MQTT_conn_err":
        errorArr[0] = 1
        if (debug_msg == 1):
            print("MQTT_conn_err")
        
    if error == "MQTT_publish_err":
        errorArr[1] = 1
        if (debug_msg == 1):
            print("MQTT_publish_err")
        
    if error == "CAN_recei_err":
        errorArr[2] = 1
        if (debug_msg == 1):
            print("CAN_recei_err")
        
    if error == "speedLimit_deny":
        errorArr[3] = 1
        if (debug_msg == 1):
            print("speedLimit_deny")
    
def clearErrReport(error):
    global errorArr
    if error == "MQTT_conn_err":
        errorArr[0] = 0
        
    if error == "MQTT_publish_err":
        errorArr[1] = 0
        
    if error == "CAN_recei_err":
        errorArr[2] = 0
        
    if error == "speedLimit_deny":
        errorArr[3] = 0

#Update data from global_data to Kafka and MQTT payload
def updatePayload():
    global global_data
    
    updateErrMsg()
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
            "core2_load": global_data["core2_load"],
            "pi_load": psutil.cpu_percent(),
            "trafficSign": TRAF_ID_MOBILE[global_data["trafficSign"]] 
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
        "frontBrakeStatus": global_data["front_break"],
        "rearBrakeStatus": global_data["rear_break"],
        "outrigger_detection": global_data["outrigger_detection"],
        "core0_load": global_data["core0_load"],
        "core1_load": global_data["core1_load"],
        "core2_load": global_data["core2_load"],
        "pi_load": psutil.cpu_percent(),
        "trafficSign":TRAF_ID_MOBILE[global_data["trafficSign"]] 
        }

    return kafka_data, mobile_data

#######################################################################
#MQTT & Kafka callbacks
#######################################################################
def mqtt_on_message(client, userdata, msg):
    global mqttClient, global_data,initDone_MQTT
    recv_msg = json.loads(str(msg.payload))
    
    #Mobile device have the highest priority
    if recv_msg['dev_ID'] == "mobile":
        global_data["msgSrc"] = "mobile"
        global_data["speed_limit"] = recv_msg ['maxSpeed']
        send_back_msg = {
            "maxSpeed": global_data["speed_limit"]
        }
        try:
            mqttClient.publish(MQTT_RECV_TOPIC,json.dumps(send_back_msg, indent=2), retain = True)
            clearErrReport("speedLimit_deny")
        except:
            pass
    elif recv_msg['dev_ID'] == "VSK":
        if (global_data["msgSrc"] == "mobile" and global_data["speed_limit"] == 0) or global_data["msgSrc"] == "VSK":
            global_data["speed_limit"] = recv_msg ['maxSpeed']
            global_data["msgSrc"] = "VSK"
            send_back_msg = {
                "maxSpeed": global_data["speed_limit"]
            }
            try:
                mqttClient.publish(MQTT_RECV_TOPIC,json.dumps(send_back_msg, indent=2), retain = True)
                clearErrReport("speedLimit_deny")
            except:
                pass
        else:
            reportErr("speedLimit_deny")
    #REMOVE in final version
    #print('Current Speed Limit: ', global_data["speed_limit"])

# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, rc):
    global mqttClient

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqttClient.subscribe(MQTT_RECV_TOPIC)

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
    global COM_Publish, MQTT_Listen, TrafSign, canBus, kafkaProducer, mqttClient,debug_msg,initDone_kafka,initDone_MQTT,retry_time,retry_cnt
    
    #Init side Threads
    COM_Publish = Thread(target = COM_Publish_Thread)
    MQTT_Listen = Thread(target = MQTT_Listen_Thread)
    TrafSign = Thread(target = TrafSign_Thread)
    
    COM_Publish.setDaemon(True)
    MQTT_Listen.setDaemon(True)
    TrafSign.setDaemon(True)

    #Init CAN bus
    canBus = can.interface.Bus(bustype='socketcan', channel=CAN_CHANNEL ,bitrate=CAN_BITRATE)
    canBus.set_filters([{"can_id":21, "can_mask":0x7FF},{"can_id":22, "can_mask":0x7FF}, {"can_id":24, "can_mask":0x7FF}, {"can_id":25, "can_mask":0x7FF}, {"can_id":26, "can_mask":0x7FF}, {"can_id":35, "can_mask":0x7FF}, {"can_id":36, "can_mask":0x7FF}, {"can_id":42, "can_mask":0x7FF}, {"can_id":16, "can_mask":0x7FF}])

    #Init Kafka
    if initDone_kafka == 0:
        try:
            kafkaProducer = KafkaProducer(bootstrap_servers=[KAFKA_HOST+":"+str(KAFKA_PORT)])
            initDone_kafka = 1
        except:
            initDone_kafka = 0
            if(debug_msg == 1):
                print("Can't connect to kafka, try to reconnect after 5s")
    
    #Init MQTT
    mqttClient= mqtt.Client("control1")
    mqttClient.on_message = mqtt_on_message
    mqttClient.on_connect = mqtt_on_connect
    if initDone_MQTT == 0:
        try:
            mqttClient.connect(MQTT_HOST,MQTT_PORT)
            clearErrReport("MQTT_conn_err")
            initDone_MQTT = 1
        except:
            initDone_MQTT = 0
            reportErr("MQTT_conn_err")
            if(debug_msg == 1):
                print("Can't connect to MQTT, try to reconnect after 5s")
            
    #Re-initialize protocol
    if (initDone_MQTT + initDone_kafka) < 1:
        time.sleep(5)
        init()
    elif (initDone_MQTT + initDone_kafka) < 2: #Retry 5 times if MQTT or Kafka connected
        if retry_cnt < retry_time:
            print('Attempt to retry: ',retry_cnt)
            retry_cnt = retry_cnt + 1
            time.sleep(5)
            init()

#Start all processess
def init_End():
    global COM_Publish, MQTT_Listen, TrafSign
    
    #Start side Threads
    COM_Publish.start()
    MQTT_Listen.start()
    TrafSign.start()


#######################################################################
#Define Main Thread, just assign above thread into main thread
#######################################################################
def main_Thread():
    CAN_Thread()

#######################################################################
#Main Program Flow
#######################################################################
if __name__ == "__main__":

        #Start CAN init
        return_value = subprocess.call(['sh', './CAN_Ini.sh'])
        time.sleep(1)
        print(return_value)
        
        #Initialize stuff
	init()
	init_End()

	#Main Thread
	main_Thread()
	sys.exit()
