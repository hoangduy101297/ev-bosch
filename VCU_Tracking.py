#import paho.mqtt.client as paho
import os
import json
import time
import can
from threading import Thread
import threading
import random
import sys
import Tkinter as tk

sys.path.insert(0,'/home/pi/EV/ev-bosch/GUI/')
import test_GUI as gui

#from test_GUI import vp_start_gui 
from can import Message
from datetime import datetime

LAT = [10.802478, 10.800770, 10.795431,
       10.796527, 10.793814, 10.801928, 10.806929]
LON = [106.640324, 106.660766, 106.655795,
       106.65460, 106.651709, 106.636633, 106.635009]
msg = [999, 999, 999, 999, 999, 999]
cnt = 0
CAN_RATE = 0.01  # 10ms
PUBLISH_RATE = 5  # 5s

DATA_READY = 0
exit_fl = 0
tk_obj = tk.Tk()
gui_obj = None
# # DEVICE CONFIG GOES HERE
# __tenantId = "t169603e0440c455a96c0e0a2b7f366f4_hub"
# __device_password = "123456"
# __hub_adapter_host = "mqtt.bosch-iot-hub.com"
# __deviceId = "duynguyen.namespace:device02"
# __clientId = __deviceId
# __authId = "duynguyen.namespace_device02"
# __certificatePath = "iothub.crt"
# __ditto_topic = "duynguyen.namespace/device02"
# __topic = "telemetry/" + __tenantId + "/" + __deviceId
# __port = 8883  # MQTT data listening port
# 
# __payloadDict = {"topic": __ditto_topic+"/things/twin/commands/modify",
#                  "headers": {"response-required": False},
#                  "path": "/features/E-Bike/properties",
#                  "value": {
#                      "Lon": 0,
#                      "Lat": 0,
#             		 "VehSpd": (random.randint(0, 100)),
#             		 "BattSt": 0,
#                      "iBattSt": 0,
#                      "BrkSt": 0,
#                      "AppSt": 0,
#                      "iMot" : 0,
#                      "Temp": 0
#                     }
#                 }


# def establishConnection():
# 	client = paho.Client(__clientId)  # create client object
# 	#self.client = paho.Client("test")
# 	client.on_publish = on_publish  # assign function to callback
# 	client.tls_set(__certificatePath)
# 	username = __authId + "@" + __tenantId
# 	client.username_pw_set(username, __device_password)
# 	client.connect(__hub_adapter_host, __port, keepalive=60)  # establishing connection
# 	#self.client.connect("10.184.150.132",1883,keepalive=60)


# def on_publish(client, userdata, result):  # create function for callback
#     print("Published data is: ")
#     DATA_READY = 0
#     pass
# 
# 
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))

# 
# def update_payload(m_lat, m_lon, mSpeed, iMot, uBat, brake, APP, temp, iBat):
#     __payloadDict["value"]["Lat"] = m_lat
#     __payloadDict["value"]["Lon"] = m_lon
#     __payloadDict["value"]["VehSpd"] = mSpeed
#     __payloadDict["value"]["BattSt"] = uBat
#     __payloadDict["value"]["iMot"] = iMot
#     __payloadDict["value"]["BrkSt"] = brake
#     __payloadDict["value"]["AppSt"] = APP
#     __payloadDict["value"]["Temp"] = temp
#     __payloadDict["value"]["iBattSt"] = iBat
#     _jsonPayload = json.dumps(__payloadDict)
#     print(_jsonPayload)
#     DATA_READY = 1


def CAN_msg_receive():
    # reserved func
    pass

def CAN_msg_send():
    # reserved func
    pass

def CAN_Thread():
    bus = can.interface.Bus(bustype='socketcan', bitrate=500000)
    while True:
        try:
            rcv_msg = bus.recv(timeout = None)			
            if(rcv_msg.arbitration_id == 19):
		print("CAN Thread: Getting new CAN Message!")
                msg = rcv_msg.data
                cnt = cnt + 1
                if(cnt > 20):
                    cnt = 0
                    try:
                        #for index in range(len(LON)):
                        update_payload(LAT[0], LON[0], msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])

                    except Exception as ex:
                        print(ex)
                        continue
			            #msg = [0,1,2,3,4,5]
			            #print("Debug: Message! Can")
        except:
            print("CAN Thread: Error CAN Message!")                        
            continue
		#time.sleep(CAN_RATE) 

# def Publish_Thread():
#     establishConnection()
#     while True:
#         if(DATA_READY):
# 	    print("Publish Thread: Data are updated, ready to be published!") 
#             #jsonPayload = json.dumps(__payloadDict)
#             ret = client.publish(__topic, jsonPayload)
# 	    if (ret):
#                 print("Publish Thread: Data Published successfully!")	
# 	    else:
# 		print("Publish Thread: Data can not be published!")
#         else:
#             pass
#         #time.sleep(PUBLISH_RATE)

def GUI_Thread():
    global gui_obj, tk_obj
    gui_obj = gui.vp_start_gui(tk_obj)
    tk_obj.mainloop()
    #thread3.join()

def test_Thread():
    cnt = 0
    while True:
        time.sleep(0.5)
        gui.GUI_callback(cnt)
        cnt = cnt + 1
        

def main():
    global thread1, thread2, thread3
    #thread1 = Thread(target = CAN_Thread)
    thread2 = Thread(target = test_Thread)
    #thread3 = Thread(target = GUI_Thread)
    
    #thread1.setDaemon(True) 
    thread2.setDaemon(True)
    #thread3.setDaemon(True)

    #thread1.start()
    thread2.start()
    #thread3.start()
    
    GUI_Thread()
    sys.exit()
    
#    while True:
#         #time.sleep(1)
#         if exit_fl == 1:
#             print('aaaa')
#             sys.exit()


if __name__ == "__main__":
    main()