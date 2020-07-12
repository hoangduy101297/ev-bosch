import can
from can import Message
import time
x = [0,0,0,0,0]

bus = can.interface.Bus(bustype='socketcan',
                        channel='can0',
                        bitrate=500000)


while True:
    for i in range(0,4):
        x[i] = x[i] + i + 1
        if x[i] > 255:
            x[i] = 0
    
    message = can.Message(arbitration_id=19, extended_id=True, data=[x[0], x[1], x[2], x[3], x[4]])
    bus.send(message)
    time.sleep(0.01)