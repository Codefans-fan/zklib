from struct import pack, unpack
from datetime import datetime, date

from zkconst import *

def zkpinwidth(self):
    """Start a connection with the time clock"""
    command = CMD_DEVICE
    command_string = '~PIN2Width'
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]

    client_length= 19
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b + buf_a
    self.zkclient.send(buf)
    try:
        #testres ='5050827D15000000D007A9E263190E007E50494E3257696474683D3900'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
    
