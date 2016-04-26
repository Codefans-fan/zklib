from struct import pack, unpack
from datetime import datetime, date

from zkconst import CMD_DEVICE,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,END_TAG

def zkworkcode(self):
    """Start a connection with the time clock"""
    command = CMD_DEVICE
    command_string = 'WorkCode'
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]

    client_length= 17
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b + buf_a + END_TAG
    self.zkclient.send(buf)
    try:
        #testres ='5050827D13000000D00711FF63190C00576F726B436F64653D3000'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
