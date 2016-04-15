from struct import pack, unpack

from zkconst import CMD_VERSION, CMD_DEVICE,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,END_TAG

def zkplatform(self):
    """Start a connection with the time clock"""
    command = CMD_DEVICE
    command_string = '~Platform'
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    client_length = 18
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    
    buf = buf_b+buf_a+END_TAG
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
        #testres = '5050827D1D000000D00731A7631909007E506C6174666F726D3D4A5A343732355F54465400'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
    

def zkplatformVersion(self):
    """Start a connection with the time clock"""
    command = CMD_DEVICE  
    command_string = '~ZKFPVersion'
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    client_length= 21
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)

    buf = buf_b+buf_a+END_TAG
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
#         if reply_id > 16:
#             testres ='5050827D18000000D007EB6B631912007E5A4B465056657273696F6E3D313000'.decode('hex')
#         else:    
#             testres ='5050827D18000000D007F36B63190A007E5A4B465056657273696F6E3D313000'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
    
def zkfirmwareVersion(self):
    command = CMD_VERSION
    command_string = ''
    client_length = 8
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    
    buf = buf_b+buf_a
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
        
#         if reply_id > 5:
#             testres = '5050827D1B000000D007FD936319110056657220362E363020286275696C6433392900'.decode('hex')
#         else:
#             testres = '5050827D1B000000D0070D946319010056657220362E363020286275696C6433392900'.decode('hex')
       
        self.data_recv =  self.zkclient.recv(1024)
        print self.data_recv.encode('hex')
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False

def zkisonlyrf(self):
    command = CMD_DEVICE
    command_string = '~IsOnlyRFMachine'
    client_length = 25
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    
    buf = buf_b+buf_a
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
        
#         testres = '5050827D1B000000D00724D7631913007E49734F6E6C7952464D616368696E653D3000'.decode('hex')
       
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
