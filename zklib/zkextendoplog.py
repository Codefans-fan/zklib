from struct import  unpack

from zkconst import CMD_DEVICE,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,END_TAG
def zkextendoplog(self,recommand=None,index=0):
    if recommand:
        command = recommand
    else:
        command = CMD_DEVICE
    
    command_string = 'ExtendOPLog'
    
    client_length = 20
    
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    
    
    
    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    
    buf = buf_b+buf_a+END_TAG
    self.zkclient.send(buf)
    try:
#         if index ==0:
#             testres = '5050827D08000000D107C7DE63190400'.decode('hex')
#         elif index == 1:
#             testres = '5050827D08000000FFFF97E663190500'.decode('hex')
#         elif index == 2:
#             testres = '5050827D08000000FFFF96E663190600'.decode('hex')
#         elif index == 3:
#             testres = '5050827D08000000FFFF95E663190700'.decode('hex')
#         elif index == 4:
#             testres = '5050827D08000000FFFF94E663190800'.decode('hex')
#         
        self.data_recv = self.zkclient.recv(1024)
        if self.checkValid(self.data_recv):
            return self.data_recv[16:]
        else: # get data error
            if index >= 4:
                return 'read extendoplog error'
            return self.extendOPLog(unpack('HHHH', self.data_recv[8:16])[0],index+1)
            
    except Exception as e:
        print e
        self.disconnect()
        return False