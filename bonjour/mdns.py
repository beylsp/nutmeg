
import struct

_TYPE_PTR = 12
_TYPE_TXT = 16
_TYPE_SRV = 33

class MDNSEntry(object):
    
    def __init__(self, queryName, queryType, queryClass):
        self.queryName = queryName
        self.queryType = queryType
        self.queryClass = queryClass

    def getQueryName(self):
        return self.queryName
    
    def getQueryType(self):
        return self.queryType
    
    def getQueryClass(self):
        return self.queryClass

class MDNSQuery(MDNSEntry):
    
    def __init__(self, queryName, queryType, queryClass):
        MDNSEntry.__init__(self, queryName, queryType, queryClass)

class MDNSRecord(MDNSEntry):
    pass

class MDNSPointerRecord(MDNSRecord):
    
    def __init__(self, domainName, recordType, recordClass, ttl):
        pass

class MDNSIncomingPacket(object):
    
    def __init__(self, packet):
        self.packet = packet
        self.offset = 0
        self.num_questions = 0
        self.num_answers = 0
        self.num_authorities = 0
        self.num_additionals = 0

        self.queries = []
        self.answers = []
        
        self.readHeader()
        self.readQuestions()
        self.readResourceRecord()
        
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
            queryName = self.readName()
            query = struct.unpack(format, self.packet[self.offset:self.offset + length])
            self.offset += length
            
            self.queries.append(MDNSQuery(queryName, query[0], query[1]))

    def readResourceRecord(self):
        format = '!HHiH'
        length = struct.calcsize(format)
        n = self.num_answers + self.num_authorities + self.num_additionals
        for i in range(0, n):
            domainName = self.readName()
            resourceRecord = struct.unpack(format, self.packet[self.offset:self.offset + length])
            
            if resourceRecord[0] == TYPE_PTR:
                self.answers.append(MDNSPointerRecord(domainName, resourceRecord[0], 
                                                      resourceRecord[1], resourceRecord[2], resourceRecord[3]))
            elif resourceRecord[0] == TYPE_TXT:
                pass
            elif resourceRecord[0] == TYPE_SRV:
                pass
            else:
                raise Exception('Invalid MDNS resource record type: %x'%resourceRecord[0])

    def readName(self):
        next = -1
        offset = self.offset
        name = ''
        while True:
            length = ord(self.packet[offset])
            offset += 1
            if length == 0:
                break
            # compressed (2 highest bits set)?
            c = length & 0xC0
            if c == 0x00:
                # no compression scheme
                name = ''.join( (name, self.packet[offset:offset+length] + '.') )
                offset += length
            elif c == 0xC0:
                # compression scheme
                compression = True
                offset = (length & 0x3F) << 8 | ord(self.packet[offset])
                next = offset + 1
            else:
                raise Exception('Bad name at position: %d'%offset)

        if next > 0:
            self.offset = next
        else:
            self.offset = offset
            
        return name
            
            
            
            
            
            
            
            
            
            
            
            
            
            