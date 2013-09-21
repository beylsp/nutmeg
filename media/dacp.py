import struct

def dacp(tag, value):
    return '%s%s%s'%(tag, struct.pack('i', len(value)), value)
