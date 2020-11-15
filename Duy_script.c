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

5/ 'Solved and Unsolved issue:'
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
	So, what is this component? Let me first tell you one story...


2/ 
	Do you still remember at the beginning of the Talk, we introduced that our vehicle has a feature called "Connectivity", which means the vehicle can communicate with the Mobile App or Web App.
	We want this communication to be anywhere, anytime, so that it`s required the vehicle be able to connect Wifi, in order to send or receive the data from the server.
	However, problem was the VCU-S just has a microcontroller and thus not possible to have a Wifi connection.

	What was the solution?

	We thought about the VCU-P, which has a microprocessor. But you know, this device is really really costly that we cannot touch. 
	So, we decided to use one Processor Module, the Raspberry Pi, or also called `the Pi`.
	Pretty sure that many of you known about this device, basically it`s just like an external processor in our system which enable the Wifi connection.
	Based on that, it will communicate with the server, data can be sent and received from the MobileApp or WebApp. 
	On the other hand, it also has the CAN driver to communicate with the Vehicle. So that, data can be transmitted between vehicle and the server, going throught the Pi.
	And finally, we give it a name, "The Central Gateway".

	The idea is simple, right? But it`s not that easy. Because there are lots of information to be transmitted between Vehicle and the User. I will quickly show you what I mean.

	Firstly, let`s just take a look again on the initial vehicle. We have the VCU-S and the INVERTER, also the RADAR and the ABS.
	Each of these components provides several data as you can see on the screen.

	From the user side, we have the MobileApp and the WebApp. Each of them will display, not all the data from vehicle, but just a sub-set.
	Of course, the displayed data sets in MobileApp and WebApp are also different.

	Moreover, some data also need to be converted between the engineer-readable to the user readable. For example, the speed read from
	ABS is in rpm, and it should be converted to Km/h when displaying on the User Apps.

	Collect all these stuffs, we designed the Central Gateway with 2 main functionalities:
		- First, it is a bridge between Vehicle and Server, help all the data stream can flow directly.
		- Secondly, it translates the data in engineering unit to the user-friendly unit and vice versa.

	So, I will show you how we could make these functionalities work.

3/
	First of all, let`s talk about the communication protocol.

	For the communication with vehicle, CAN is the best choise as it allows the gateway to easily talk to any components 
	in the vehicle by the CAN network.

	And for the server, when we start developing the Gateway, the WebApp and MobileApp had almost done their basic software.
	So we chose the protocol as following to them, which is Kafka for WebApp and MQTT for MobileApp.
	But I wont go to detail is these protocols. We actually just use the libraries. What we focus in is the handling of multiple
	data thread.  


	One lucky thing is, all the software libraries we need for CAN, MQTT and Kafka are available in Python. So that we quickly 
	decided to use Python to develop the Gateway software.

	Ok, Let`s take a look on this.
	I have here all the input data of the gateway, from the vehicle side. Let`s see, we have speed, odometer, status of vehicle inputs,...
	We want to send these data to the server. 


	





