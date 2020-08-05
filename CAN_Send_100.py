import can
from can import Message
import time
import math
x = 0
k = 0
j = 0

bus = can.interface.Bus(bustype='socketcan',
                        channel='can0',
                        bitrate=500000)


while True:
    j = j + 1
    if(j == 50):
        k = k + 1 if k <= 359 else 0
        x = int((math.cos(k/3.14)+1)*50)
        j = 0
    

    print(x)
    message = can.Message(arbitration_id=19, extended_id=True, data=[x, x, x, x, x])
    bus.send(message)
    time.sleep(0.01)