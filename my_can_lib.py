from __future__ import division

global TRAF_ID,prev_T15_st,cnt,str_cnt,stop_tranfer_data
TRAF_ID = ["SpdLim","NoLim","Pedes","Stop","NoTraf"]

def updateDataVCU1(new_data, des):
    des['outrigger_detection'] = 0 if new_data[0] & 0x02 == 0x02 else 1
    des['front_break'] = 1 if new_data[0] & 0x04 == 0x04 else 0
    des['rear_break'] = 1 if new_data[0] & 0x01 == 0x01 else 0
    des['odo_meter'] = (new_data[4]*256*256*256 + new_data[5]*256*256+ new_data[6]*256 + new_data[7])/1000

def updateDataVCU2(new_data, des):
    global prev_T15_st,cnt,str_cnt,stop_tranfer_data
    des['battery_status'] = (new_data[0]*4 + ((new_data[1]&0xC0)>>6))/10
    des['t15_st'] = 1 if new_data[1] & 0x04 == 0x04 else 0
    if des['t15_st'] == 0:
        if prev_T15_st == 1:
            str_cnt = 1
        if str_cnt == 1:
            cnt = cnt + 1
            if cnt >= 10:
                stop_tranfer_data = 1
                str_cnt = 0
    else:
        str_cnt = 0
        cnt = 0
        stop_tranfer_data = 0
    prev_T15_st = des['t15_st']

def updateDataIVT1(new_data, des):
    des['battery_voltage'] = (new_data[2]*2)/10

def updateDataIVT2(new_data, des):
    des['battery_current'] = new_data[0] if new_data[0] <= 127 else 0

def updateDataCoreLoad0(new_data, des):
    global stop_tranfer_data
    if stop_tranfer_data == 0:
        des['core0_load'] = (new_data[0]*256 + new_data[1])/100
    else:
        des['core0_load'] = 0
    #print(new_data.value)
    des['front_wh_speed'] = round((new_data[6]*256 + new_data[7])*0.05625,2)

def updateDataCoreload1(new_data, des):
    global stop_tranfer_data
    if stop_tranfer_data == 0:
        des['core1_load'] = (new_data[0]*256 + new_data[1])/100
    else:
        des['core1_load'] = 0
    #print(new_data.value)
    des['rear_wh_speed'] = round((new_data[6]*256 + new_data[7])*0.05625,2)
    
def updateDataCoreLoad2(new_data, des):
    global stop_tranfer_data
    if stop_tranfer_data == 0:
        des['core2_load'] = (new_data[0]*256 + new_data[1])/100
    else:
        des['core2_load'] = 0

def updateDataABS(new_data, des):
    #des['rear_wh_speed'] = round((new_data[0]*256 + new_data[1])*0.05625,2)
    pass

def updateDataRADAR(new_data, des):
    pass

def updateDataPI1(new_data, des):
    pass

def updateDataPI2(new_data, des):
    des["trafficSign"] = TRAF_ID[new_data[2]]
    des["newTrafSign_flg"] = 1
    if new_data[2] == 0:
        des["speed_limit_traf"] = 30        
        if des["spdFamilyShare"] > 30:
            des["speed_limit"] = 30
        
    if new_data[2] == 1:
        des["speed_limit_traf"] = 100
        des["speed_limit"] = des["spdFamilyShare"]
