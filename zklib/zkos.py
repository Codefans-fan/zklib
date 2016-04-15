from struct import unpack

from zkconst import CMD_DEVICE,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,END_TAG


def zkos(self):
    """Start a connection with the time clock"""
    command = CMD_DEVICE
    command_string = '~OS'
    chksum = 0
    session_id = unpack('HHHH', self.data_recv[8:16])[2]
    
    reply_id = unpack('HHHH', self.data_recv[8:16])[3]
    client_length = 12

    buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
    buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
    
    buf = buf_b+buf_a + END_TAG
    self.zkclient.send(buf)
    try:
#         if reply_id > 15:
#             testres = '5050827D0E000000D007B651631914007E4F533D3100'.decode('hex')
#         else:
#             testres = '5050827D0E000000D007C851631902007E4F533D3100'.decode('hex')
        self.data_recv= self.zkclient.recv(1024)

        return self.data_recv[16:]
    except Exception as e:
        print e
        self.disconnect()
        return False
        