#Data position
CAN_pos = {
    'VCU1':{
        'spd':0,
        'brk':1
    },
    
    'VCU2':{
        'ubat':0,
        'app':1
    },
    
    'INVERTER':{
    },
    
    'ABS':{
    },
    
    'PI':{
    },
    
    'RADAR':{
    }
}


def UpdateDataFromCan(des, src, data):
    for x in CAN_pos[src]:
        des[x] = data[CAN_pos[src][x]]