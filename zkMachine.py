
from zklib import zklib

import threading


import types



# print current lock user 
def addRecord(record):
    print record



zk = zklib.ZKLib("172.69.8.4", 4370)

res = zk.connect()
if res:
    while True:
        data = zk.zkrecvCurrentAtt()   #(uid, time)
        if data:
            if type(data) == types.BooleanType:
                continue
            t = threading.Thread(target=addRecord,args=(data,))
            t.start()


#zk.disconnect()


