from StringIO import StringIO
import struct

class TLV(object):
    
    def __init__(self, tag, value):
        if isinstance(value, list):
            value = ''.join(value)
    
        self.tlv = '%s%s%s'%(tag, struct.pack('>i', len(value)), value)

    def tostring(self):
        return self.tlv
