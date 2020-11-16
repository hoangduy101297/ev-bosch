/* Script written by Duy - Do not copy =))) */

1/ 'Thanks and continue the presentation:'

2/  'Demand/Requirement: + problem'
	- Connectivity 

	-Problem:
		- Input & output of Gatewate
		- COM directions

	 -> Central Gatewate function

-> 3/ 'Solution + SW design:'
	- Tech used: Communication Protocol [Kafka/ MQTT]
	- Python
	- Data Structure [how to be flexible]
	- Threading [how to proceed multiple data stream]
	- From Main thread coming to others

4/ 'Solved and Unsolved issue:'
    - Solved:
		+ Different formats & protocol between VCU, IVT, MobileApp & VSK
		+ Threading

	- Unsolved:
		+ Delay time [mention: MQTT is faster than Kafka]
		+ Software is not robust: behavior when CAN timeout, MQTT/ Kafka timeout, ...

/*------------------------------------------------------------------*/
1/
	Thanks a. Tùng for such an interesting sharing on the VCU software. I believe that everyone here is feeling really excited right now.

	Alright guys, let`s come with me to the last component in our TechTalk today, in which the software is also developed 100% by our EJV associates. 
	So, what is this component? We will know soon...


2/ 
	Do you still remember at the beginning of the Talk, we introduced that our vehicle has a feature called "Connectivity", 
	which means the vehicle can communicate with the Mobile App or Web App.
	We want this communication to be anywhere, anytime, so that it`s required the vehicle be able to connect Wifi, 
	in order to send or receive the data from the server.
	However, problem was the VCU-S just has a microcontroller and thus not possible to have a Wifi connection.

	What was the solution?

	We thought about the VCU-P, which has a microprocessor. But you know, this device is really really costly that we cannot touch. 
	So, we decided to use one Embedded Computer, the Raspberry Pi, or also called `the Pi`.
	Pretty sure that many of you known about this device, basically it`s just like an external processor in our system which enable the Wifi connection.
	Based on that, it will communicate with the server, data can be sent and received from the MobileApp or WebApp. 
	On the other hand, it also has the CAN driver to communicate with the Vehicle. So that, data can be transmitted between vehicle and the server, going throught the Pi.
	And finally, we give it a name, "The Central Gateway".

	The reason why we choose MQTT and Kafka is just because when we start developing the Gateway, the WebApp and MobileApp had almost done their basic software.
	So we chose the protocol as following to them.
	And why the CAN?
	Because is the best choise as it allows the gateway to easily talk to any components in the vehicle.

	One lucky thing is, all the software libraries we need for CAN, MQTT and Kafka are available in Python. So that we quickly 
	decided to use Python to develop the Gateway software.

	The idea is simple, right? But it`s not that easy. 
	Because there are lots of information to be transmitted between Vehicle and the User. I will quickly show you what I mean.

3/
	Ok, Let`s take a look on this.

	Firstly, in the initial vehicle, we have the VCU-S and the INVERTER. The RADAR and the ABS were tentative so I do not put them here.
	Each of these components provides several data as you can see on the screen, and via the CAN network.

	We want to send these data to the server to display on WebApp and Mobile App.
	Since we are using MQTT and Kafka protocols, there is a term called `topic`.
	So, each node connecting to the MQTT or Kafka host, can publish message to the topic, this is called Publisher.
	Then, there are also subcribers who subcribed to the topic. And when there is new message coming in the topic, the subcribers
	can read it by a callback function.

	By this way, the vehicle data is transmitted from the vehicle to gateway via CAN, and then continued from gateway to
	WebApp and MobileApp via MQTT and Kafka.

	It`s clear, right?

	So, also in another feature of our vehicle, Family Share, we want that the user can set the speed limitation via the MobileApp.
	So, we have another MQTT topic here, `spd-limit-topic`. And now, MobileApp is the publisher and 
	the Gateway will subcribe to this topic.

	Seem complicated now? But it`s not all.

	We still have one more input, is the AI camera. In technical view, the camera should be processed also by the CAN. 
	However, we do not have enough resource to run image processing in this Pi, so we use another Pi to detect traffic sign,
	and send the result to this central gateway temporarily via CAN. Please note, just temporarily.

	Finally, the input from AI camera and SpdLimit from user will be forwarded to the VCU to control the vehicle.

	So, that`s all the input and output of the Gateway. 
	When we have a picture like this, the implementation is really easy, I would say.

	
