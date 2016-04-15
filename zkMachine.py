
import time
from zklib import zklib


zk = zklib.ZKLib("172.69.8.4", 4370)

res = zk.connect()

#zk.zkrecv()

# zk.zksendCache(0)
# zk.zksendCache(1)

time.sleep(5)
zk.disconnect()

#zk.disconnect()


