# import the library
import can
import time


def can_proc_100ms(bus):
    """Send using ModifiableCyclicTaskABC."""
    print("Starting ...")
    msg = can.Message(arbitration_id=0x19, data=[0, 0, 0, 0, 0, 0, 0, 0])
    task = bus.send_periodic(msg, 0.10)
    if not isinstance(task, can.ModifiableCyclicTaskABC):
        print("This interface doesn't seem to support modification")
        task.stop()
        return
    time.sleep(1)
    print("Changing data...")
    while True:
        for x in range(8):
            try:
                msg.data[x] += 1
            except:
                pass
        task.modify_data(msg)
        time.sleep(0.1)
        
def main():
    bus = can.Bus(interface='socketcan',
                  channel='can0',
                  receive_own_messages=True)

    reset_msg = can.Message(arbitration_id=0x00, 
                                data=[0, 0, 0, 0, 0, 0, 0, 0],
                                is_extended_id=False)
    bus.send(reset_msg, timeout=0.2)

    can_proc_100ms(bus)


if __name__ == "__main__":
    main()
