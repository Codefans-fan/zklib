from socket import socket, AF_INET,SOCK_STREAM

import time
from struct import unpack,pack

from zkconnect import zkconnect,zkdisconnect
from zkversion import zkversion
from zkos import zkos
from zkextendfmt import zkextendfmt,zkuserextfmt
from zkextendoplog import zkextendoplog
from zkplatform import  zkfirmwareVersion,zkplatformVersion,zkplatform, zkisonlyrf
from zkworkcode import zkworkcode
from zkssr import zkssr
from zkpin import zkpinwidth
from zkface import zkfaceon
from zkfreedata import zkfinalaws,zkfreedata
from zkconst import USHRT_MAX,CMD_ACK_OK,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,parse_time
class ZKLib:
    
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.zkclient = socket(AF_INET, SOCK_STREAM)
        self.data_recv = ''
        self.userdata = []
        self.attendancedata = []
        
        
    def createChkSum(self, p):
        """This function calculates the chksum of the packet to be sent to the 
        time clock

        Copied from zkemsdk.c"""
        l = len(p)
        chksum = 0
        while l > 1:
            chksum += unpack('H', pack('BB', p[0], p[1]))[0]
            
            p = p[2:]
            if chksum > USHRT_MAX:
                chksum -= USHRT_MAX
            l -= 2
        
        
        if l:
            chksum = chksum + p[-1]
            
        while chksum > USHRT_MAX:
            chksum -= USHRT_MAX
        
        chksum = ~chksum
        
        while chksum < 0:
            chksum += USHRT_MAX
        
        return pack('H', chksum)


    def createHeader(self, command, chksum, session_id, reply_id,command_string):
        """This function puts a the parts that make up a packet together and 
        packs them into a byte string"""
        buf = pack('HHHH', command, chksum,
            session_id, reply_id)
          
        buf = unpack('8B'+'%sB' % len(command_string), buf+command_string)
          
        chksum = unpack('H', self.createChkSum(buf))[0]
        #print unpack('H', self.createChkSum(buf))
        reply_id += 1
        if reply_id >= USHRT_MAX:
            reply_id -= USHRT_MAX
        buf = pack('HHHH', command, chksum, session_id, reply_id)
        return buf + command_string
    
    def createCacheHeader(self, command, chksum, session_id, reply_id,command_string):
        buf = pack('HHHH', command, chksum,
            session_id, reply_id)
          
        buf = unpack('8B'+'%sB' % len(command_string), buf+command_string)
          
        chksum = unpack('H', self.createChkSum(buf))[0] +1
        #print chksum
        #print unpack('H', self.createChkSum(buf))
        reply_id += 1
        if reply_id >= USHRT_MAX:
            reply_id -= USHRT_MAX
        buf = pack('HHHH', command, chksum, session_id, reply_id)
        return buf + command_string
    
    def checkValid(self, reply):
        """Checks a returned packet to see if it returned CMD_ACK_OK,
        indicating success"""
        command = unpack('HHHH', reply[8:16])[0]

        if command == CMD_ACK_OK:
            self.isAlive = True
            print "CMD_ACK_OK"
            return True
        else:
            return False
    
    
    def createtop(self,top1,top2,top3,top4):
        return pack('HHHH', top1, top2, top3, top4)
        
       
    def connect(self):
        self.zkclient.connect_ex(self.address)
        time.sleep(0.1)
        zkconnect(self)
        time.sleep(0.1)
        firmwareVersion = self.firmwareVersion()
        time.sleep(0.1)
        os = self.osversion()
        time.sleep(0.1)
        extendfmt = self.extendFormat()
        time.sleep(0.1)
        extendoplog = self.extendOPLog()
        time.sleep(0.1)
        
        platform = self.platform()
        time.sleep(0.1)
        fmversion = self.fmVersion()
        time.sleep(0.1)
        
        freedata = self.freeData()
        time.sleep(0.1)
        
        workcode = self.workCode()
        time.sleep(0.1)
        fil = self.finalaws()
        return self.checkValid(self.data_recv)
        
    def disconnect(self):
        return zkdisconnect(self)
        
    def version(self):
        return zkversion(self)
        
    def osversion(self):
        return zkos(self)
        
    def extendFormat(self):
        return zkextendfmt(self)
    
    def userExtFmt(self):
        return zkuserextfmt(self)
    
    def extendOPLog(self, recommand=None,index=0):
        return zkextendoplog(self,recommand=recommand,index=index)
    
    def platform(self):
        return zkplatform(self)
    
    def fmVersion(self):
        return zkplatformVersion(self)
    
    def finalaws(self):
        return zkfinalaws(self)
    
    def firmwareVersion(self):
        return zkfirmwareVersion(self)
    
    def isonlyRFMachine(self):
        return zkisonlyrf(self)
    
    def workCode(self):
        return zkworkcode(self)
        
    def ssr(self):
        return zkssr(self)
    
    def pinWidth(self):
        return zkpinwidth(self)
    
    def faceFunctionOn(self):
        return zkfaceon(self)
    
    def freeData(self):
        return zkfreedata(self)

    def zkrecvCurrentAtt(self):
        try:
            data = self.zkclient.recv(1024)
            res = unpack('HHHH',data[8:16])
            if res[0] == 500 and res[2] == 2: #simple check 
                att_log = self.zksendCache(0)
                self.zksendCache(1)
                return att_log
            elif res[3] != 0:
                self.data_recv = data
                print data[16:]
                return True
        except Exception as e:
            self.disconnect()
    
    
    def zksendCache(self,index):
        command = 2000
        command_string = ''
        client_length = 8
        chksum = 0
        session_id = unpack('HHHH', self.data_recv[8:16])[2]
        reply_id = 0
    
        buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
    
        buf_a = self.createCacheHeader(command, chksum, session_id,reply_id,command_string)
        buf = buf_b+buf_a
        self.zkclient.send(buf)
        try:
            #testres = '5050827D15000000D0075ECB631903007E457874656E64466D743D3000'.decode('hex')
            if index == 0:
                data = self.zkclient.recv(1024)
                # get att log time
                if unpack('HHHH', data[:8])[2] > 40:
                    uid = data[16:18].split('\x00', 1)[0]
                    lock_time = parse_time(data[42:48].encode('hex'))
                    return (uid, lock_time.strftime('%Y-%m-%d %H:%M:%S'))
            return None
        except Exception as e:
            print e
            self.disconnect()
            return False
