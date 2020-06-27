import paho.mqtt.client as paho
import os
import json
import time
import can
import threading
import random

from can import Message
from datetime import datetime



LAT = [10.802478, 10.800770, 10.795431, 10.796527, 10.793814, 10.801928, 10.806929]
LON = [106.640324, 106.660766, 106.655795, 106.65460, 106.651709, 106.636633, 106.635009]
msg = [999,999,999,999,999,999]
cnt = 0
CAN_RATE = 0.01 # 10ms
PUBLISH_RATE = 5 #5s

class myHandlingThread (threading.Thread):

	# DEVICE CONFIG GOES HERE
	__tenantId = "t169603e0440c455a96c0e0a2b7f366f4_hub"
	__device_password = "123456"
	__hub_adapter_host = "mqtt.bosch-iot-hub.com"
	__deviceId = "duynguyen.namespace:device02"
	__clientId = __deviceId
	__authId = "duynguyen.namespace_device02"
	__certificatePath = "iothub.crt"
	__ditto_topic = "duynguyen.namespace/device02"
	__topic = "telemetry/" + __tenantId + "/" + __deviceId
	__port = 8883 #MQTT data listening port

	__payloadDict = {"topic":__ditto_topic+"/things/twin/commands/modify",
			"headers":{"response-required": False},
			"path": "/features/E-Bike/properties",
			"value" : {
					"Lon":0,
					"Lat":0,
					"VehSpd": (random.randint(0, 100)),
					"BattSt":0,
					"iBattSt":0,
					"BrkSt":0,
					"AppSt":0
				}
			}
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
		
	def establishConnection(self):
		self.client = paho.Client(self.__clientId) #create client object
		#self.client = paho.Client("test")
		self.client.on_publish = self.on_publish #assign function to callback
		self.client.tls_set(self.__certificatePath)
		self.username = self.__authId + "@" + self.__tenantId
		self.client.username_pw_set(self.username, self.__device_password)
		self.client.connect(self.__hub_adapter_host, self.__port, keepalive=60) #establishing connection
		#self.client.connect("10.184.150.132",1883,keepalive=60)
	def on_publish(self,client, userdata, result): #create function for callback
		print("published data is : ")
		pass

	def updatePayload(self, m_lat, m_lon, mSpeed,iMot, uBat, brake, APP, temp, iBat):
		self.__payloadDict["value"]["Lat"]= m_lat
		self.__payloadDict["value"]["Lon"]= m_lon
		self.__payloadDict["value"]["VehSpd"]= mSpeed
		self.__payloadDict["value"]["BattSt"]= uBat
		self.__payloadDict["value"]["iMot"]= iMot
		self.__payloadDict["value"]["BrkSt"]= brake
		self.__payloadDict["value"]["AppSt"]= APP
		self.__payloadDict["value"]["Temp"]= temp
                self.__payloadDict["value"]["iBat"]= iBat	
		self.jsonPayload=json.dumps(self.__payloadDict)
		#time.sleep(PUBLISH_RATE)
		print(self.jsonPayload)
		return self.client.publish(self.__topic, self.jsonPayload)
if __name__ == "__main__":

	handlingThreadObject = myHandlingThread(1)
	handlingThreadObject.start()
	handlingThreadObject.establishConnection()	
        bus = can.interface.Bus(bustype='socketcan',bitrate=500000)
	while True:
		try:
			rcv_msg = bus.recv(timeout = None)			
			if(rcv_msg.arbitration_id == 19):
                            msg = rcv_msg.data
                            cnt = cnt + 1
                            if(cnt > 20):
                                cnt = 0
                                try:
                                    #for index in range(len(LON)):
                                    ret = handlingThreadObject.updatePayload(LAT[0], LON[0], msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
                                        #ret = handlingThreadObject.updatePayload(LAT[index], LON[index], msg[0], msg[1], msg[2], msg[3], msg[4], msg[5])

                                    if(ret):
                                        print("Debug: Published Message Successfully!")
                                    else:
                                        print("Error: Failed to publish Message!")
                                except Exception as ex:
                                    print(ex)
                                    continue
			#msg = [0,1,2,3,4,5]
			#print("Debug: Message! Can")
		except:
			print("Error: Reading CAN Message!")                        
		#try:
		
		#except :
			#print("Error: Establishing Connection Unsuccessfully!")
			#break


		time.sleep(CAN_RATE)
