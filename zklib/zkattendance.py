from struct import pack, unpack

from zkconst import CMD_ATTLOG_RQ,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,END_TAG,CMD_ATTLOG_RQ_PRE,CMD_ATTLOG_RQ_START
from zkconst import decode_time,reverseHex

def getAttendanceRQ(self):
    command = CMD_ATTLOG_RQ
    command_string = ''
    client_length = 12
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b+buf_a+END_TAG+END_TAG + END_TAG + END_TAG
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
        #testres = '5050827D15000000D0075ECB631903007E457874656E64466D743D3000'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False


def preGetAttendance(self):
    command = CMD_ATTLOG_RQ_PRE
    command_string = pack('HHHH',3329,0,0,0)
    client_length = 19
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b+buf_a+END_TAG+END_TAG+END_TAG
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
        #testres = '5050827D15000000D0075ECB631903007E457874656E64466D743D3000'.decode('hex')
        self.data_recv = self.zkclient.recv(1024)
        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False


def parse_attlog(zkclient,datasize):
    logs = zkclient.recv(datasize)
    #the first 12 is not necessary
    logs = logs[12:]
    
    while len(logs) > 0:
        uid, tmp, timestamp, space = unpack( '1s26s4s9s', logs.ljust(40)[:40] )
        
        userid = int(uid.encode('hex'),16)
        userlocktime = decode_time( int( reverseHex( timestamp.encode('hex') ), 16 ) )

        print userid, userlocktime

        logs = logs[40:]
    



def _attlog_data(zkclient):
    recv = zkclient.recv(8)
    
    attdatasize = unpack('HHHH', recv)[2]
    if attdatasize == 1016:
        parse_attlog(zkclient,attdatasize)
        _attlog_data(zkclient) # continue recv
    else:
        parse_attlog(zkclient,attdatasize)
      
    


def getAttendance(self):
    command = CMD_ATTLOG_RQ_START
    command_string = pack('HHHH',0,0,65472,0)
    client_length = 16
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    buf = buf_b+buf_a
    print buf.encode('hex')
    self.zkclient.send(buf)
    try:
        #testres = '5050827D15000000D0075ECB631903007E457874656E64466D743D3000'.decode('hex')
        self.data_recv = self.zkclient.recv(24)
        #
        attlogs = _attlog_data(self.zkclient)
        
        return attlogs
    except Exception as e:
        print e
        self.disconnect()
        return False


