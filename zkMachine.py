
from zklib import zklib

import threading


import types



# print current lock user 
def addRecord(record):
    print record



zk = zklib.ZKLib("172.69.8.4", 4370)
res = zk.connect()


temp = 0 # flag to disconnect
if res:
    while temp < 4:
        data = zk.zkrecvCurrentAtt()   #(uid, time)
        if data:
            if type(data) == types.BooleanType:
                continue
            t = threading.Thread(target=addRecord,args=(data,))
            t.start()
            temp += 1





#zk.disconnect()


