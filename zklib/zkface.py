from struct import pack, unpack
from datetime import datetime, date

from zkconst import *

def zkfaceon(self):
    """Start a connection with the time clock"""
    command = CMD_DEVICE
    command_string = 'FaceFunOn'
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]

    client_length= 18
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b + buf_a
    print buf.encode('hex')
    #self.zkclient.send(buf)
    try:
        testres ='5050827D08000000D107BCDE63190F00'.decode('hex')
        self.data_recv = testres   # self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
    
