from datetime import datetime

USHRT_MAX = 65535

MACHINE_PREPARE_DATA_1 = 20560
MACHINE_PREPARE_DATA_2 = 32130
CMD_FINAL_AWS = 500



CMD_CONNECT = 1000
CMD_EXIT = 1001
CMD_ATTLOG_RQ = 1003

CMD_ATTLOG_RQ_PRE = 1503
CMD_ATTLOG_RQ_START = 1504



CMD_ACK_OK = 2000
CMD_ACK_ERROR = 2001
CMD_ACK_DATA = 2002

CMD_PREPARE_DATA = 1500
CMD_DATA = 1501


CMD_VERSION = 1100
CMD_DEVICE = 11

CMD_FREE_DATA = 69


END_TAG = '00'.decode('hex')


def encode_time(t):
    """Encode a timestamp send at the timeclock

    copied from zkemsdk.c - EncodeTime"""
    d = ( (t.year % 100) * 12 * 31 + ((t.month - 1) * 31) + t.day - 1) *\
         (24 * 60 * 60) + (t.hour * 60 + t.minute) * 60 + t.second

    return d



def decode_time(t):
    """Decode a timestamp retrieved from the timeclock

    copied from zkemsdk.c - DecodeTime"""
    second = t % 60
    t = t / 60

    minute = t % 60
    t = t / 60

    hour = t % 24
    t = t / 24

    day = t % 31+1
    t = t / 31

    month = t % 12+1
    t = t / 12

    year = t + 2000

    d = datetime(year, month, day, hour, minute, second)

    return d

def parse_time(t):
    
    year = int(t[:2],16)+2000
    month = int(t[2:4],16)
    day = int(t[4:6],16)
    hour = int(t[6:8],16)
    minute = int(t[8:10],16)
    second = int(t[10:12],16)
    
    return datetime(year, month, day, hour, minute, second)


def reverseHex(hexstr):
    tmp = ''
    for i in reversed( xrange( len(hexstr)/2 ) ):
        tmp += hexstr[i*2:(i*2)+2]
    
    return tmp

if __name__=='__main__':
    print   decode_time(int(reverseHex("ED 43 99 1E ".replace(' ', '')),16))
    #print parse_time('10040f110d36').strftime('%Y-%m-%d %H:%M:%S')
