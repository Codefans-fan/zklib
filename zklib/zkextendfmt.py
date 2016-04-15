from struct import pack, unpack

from zkconst import CMD_DEVICE,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,END_TAG

def zkextendfmt(self):
    command = CMD_DEVICE
    command_string = '~ExtendFmt'
    client_length = 19
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b+buf_a+END_TAG
    self.zkclient.send(buf)
    try:
        #testres = '5050827D15000000D0075ECB631903007E457874656E64466D743D3000'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
    
    
def zkuserextfmt(self):
    command = CMD_DEVICE
    command_string = '~UserExtFmt'
    client_length = 20
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b+buf_a
    self.zkclient.send(buf)
    try:
        testres = '5050827D16000000D007F4BE631910007E55736572457874466D743D3100'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False