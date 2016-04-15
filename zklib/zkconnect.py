from struct import  unpack

from zkconst import CMD_CONNECT, MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,USHRT_MAX,CMD_EXIT


def zkconnect(self):
    """Start a connection with the time clock"""
    command = CMD_CONNECT
    command_string = ''
    chksum = 0
    session_id = 0
    reply_id = -1 + USHRT_MAX
    client_length = 8
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,
        reply_id,command_string)
    
    
    buf = buf_b+buf_a
    self.zkclient.send(buf)
    try:
        #testres = '5050827D08000000D007CCDE63190000'.decode('hex')
        
        self.data_recv = self.zkclient.recv(1024)
        
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
def zkdisconnect(self):
    """Disconnect from the clock"""
    command = CMD_EXIT
    command_string = ''
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    client_length = 8
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    
    buf = buf_b+buf_a
    self.zkclient.send(buf)
    try:
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.zkclient.close()
        return False
    
