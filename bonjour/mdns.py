
import struct

class MDNSIncomingPacket(object):
    
    def __init__(self, packet):
        self.packet = packet
        self.offset = 0
        
        self.readHeader()
        self.readQuestions()
        
        
    def readHeader(self):
        format = '!HHHHHH'
        length = struct.calcsize(format)
        header = struct.unpack(format, self.packet[self.offset:self.offset + length])
        self.offset += length
        
        self.identification = header[0]
        self.flags = header[1]
        self.num_questions = header[2]
        self.num_answers = header[3]
        self.num_authorities = header[4]
        self.num_additionals = header[5]
        
    def readQuestions(self):
        format = '!HH'
        length = struct.calcsize(format)
        for i in range(0, self.num_questions):
            queryName = self.readQueryName()
            question = struct.unpack(format, self.packet[self.offset:self.offset + length])
            self.offset += length
        
    def readQueryName(self):
        pass    