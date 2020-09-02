def updateDataVCU1(new_data, des):
    des['outrigger_detection'] = 1 if new_data[0] & 0x02 == 0x02 else 0
    des['front_break'] = 1 if new_data[0] & 0x01 == 0x01 else 0
    des['rear_break'] = des['front_break']

def updateDataVCU2(new_data, des):
    des['battery_status'] = new_data[0]*4 + new_data[1]>>6

def updateDataIvt1(new_data, des):
    spd = new_data[0]*255 + new_data[1]
    des['front_wh_speed'] = spd
    des['rear_wh_speed'] = spd
    des['battery_voltage'] = (new_data[2]*2)/10
    des['error_message'] = 'Inverter Temperature: ' + str(new_data[5])

def updateDataCoreLoad0(new_data, des):
    des['core0_load'] = new_data[0]*255 + new_data[1]

def updateDataCoreLoad1(new_data, des):
    des['core1_load'] = new_data[0]*255 + new_data[1]

def updateDataCoreLoad2(new_data, des):
    des['core2_load'] = new_data[0]*255 + new_data[1]       

def updateDataIvt2(new_data, des):
    des['battery_current'] = new_data[0]

def updateDataAbs(new_data, des):
    pass

def updateDataRadar(new_data, des):
    pass