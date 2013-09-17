import struct
import socket

_TYPE_A         = 1
_TYPE_NS        = 2
_TYPE_MD        = 3
_TYPE_MF        = 4
_TYPE_CNAME     = 5
_TYPE_SOA       = 6
_TYPE_MB        = 7
_TYPE_MG        = 8
_TYPE_MR        = 9
_TYPE_NULL      = 10
_TYPE_WKS       = 11
_TYPE_PTR       = 12
_TYPE_HINFO     = 13
_TYPE_MINFO     = 14
_TYPE_MX        = 15
_TYPE_TXT       = 16
_TYPE_AAAA      = 28
_TYPE_SRV       = 33
_TYPE_RRSIG     = 46
_TYPE_DNSKEY    = 48
_TYPE_AXFR      = 252
_TYPE_ANY       = 255

_CLASS_IN       = 1
_CLASS_CS       = 2
_CLASS_CH       = 3
_CLASS_HS       = 4
_CLASS_NONE     = 254
_CLASS_ANY      = 255

# MDNS header opcodes
STANDARD_QUERY        = 0
INVERSE_QUERY         = 1
SERVER_STATUS_REQUEST = 2

# masks
_FLAGS_QR_MASK      = 0x8000
_FLAGS_QR_QUERY     = 0x0000
_FLAGS_QR_RESP      = 0x8000

_FLAGS_OPCODE_MASK  = 0x7800

_CLASS_MASK = 0x7FFF

# MDNS query types mapping
_TYPES = {_TYPE_A: "A",
          _TYPE_NS: "NS",
          _TYPE_MD: "MD",
          _TYPE_MF: "MF",
          _TYPE_CNAME: "CNAME",
          _TYPE_SOA: "SOA",
          _TYPE_MB: "MB",
          _TYPE_MG: "MG",
          _TYPE_MR: "MR",
          _TYPE_NULL: "NULL",
          _TYPE_WKS: "WKS",
          _TYPE_PTR: "PTR",
          _TYPE_HINFO: "HINFO",
          _TYPE_MINFO: "MINFO",
          _TYPE_MX: "MX",
          _TYPE_TXT: "TXT",
          _TYPE_AAAA: "AAAA",
          _TYPE_SRV: "SRV",
          _TYPE_RRSIG: "RRSIG",
          _TYPE_DNSKEY: "DNSKEY",
          _TYPE_AXFR: "AXFR",
          _TYPE_ANY: "ANY" }

_CLASSES = {_CLASS_IN: "IN",
            _CLASS_CS: "CS",
            _CLASS_CH: "CH",
            _CLASS_HS: "HS",
            _CLASS_NONE: "NONE",
            _CLASS_ANY: "ANY"}

_INDENT = 2*' '
_DAYS_IN_SEC = 86400 
_HOURS_IN_SEC = 3600
_MINUTES_IN_SEC = 60

PRIOR_WEIGHT_PORT_LEN = 6

class MDNSRecord(object):

    def __init__(self, name, type, clazz):
        self.name = name
        self.type = type
        self.clazz = clazz & _CLASS_MASK

    def getName(self):
        return self.name
    
    def getType(self):
        return self.type
    
    def getClass(self):
        return self.clazz

class MDNSQueryRecord(MDNSRecord):
    
    def __init__(self, name, type, clazz):
        MDNSRecord.__init__(self, name, type, clazz)

    def __repr__(self):
        return '%s: type %s, class %s\n'%(self.name, _TYPES[self.type], _CLASSES[self.clazz])

class MDNSResourceRecord(MDNSRecord):
    
    def __init__(self, name, recordType, recordClass, ttl, resourceDataLength):
        MDNSRecord.__init__(self, name, recordType, recordClass)

        self.ttl = ttl
        self.resourceDataLength = resourceDataLength

    def __repr__(self, level=1):
        _str = ''
        _str += '%s%s: type %s, class %s\n'%(level*_INDENT, self.name, _TYPES[self.type], _CLASSES[self.clazz])
        level+= 1
        _str += '%sTime to live: %s\n'%(level*_INDENT, self._ttl())
        _str += '%sData length: %s\n'%(level*_INDENT, self.resourceDataLength)
        
        return _str

    def _ttl(self):
        _str = ''
        days, seconds = divmod(self.ttl, _DAYS_IN_SEC)
        hours, seconds = divmod(seconds, _HOURS_IN_SEC)
        minutes, seconds = divmod(seconds, _MINUTES_IN_SEC)

        if days != 0:
            _str += '%d days '%days
        if hours != 0:
            _str += '%d hours'%hours
        if minutes != 0:
            _str += ' %d minutes'%minutes
        if seconds != 0:
            _str += ' %d seconds'%seconds

        return _str

class MDNSAddressRecord(MDNSResourceRecord):

    def __init__(self, name, recordType, recordClass, ttl, resourceDataLength, address):
        MDNSResourceRecord.__init__(self, name, recordType, recordClass, ttl, resourceDataLength)

        self.address = address
        
    def __repr__(self, level=1):
        _str = ''
        _str += MDNSResourceRecord.__repr__(self, level)

        level += 1        
        _str += '%sAddr: %s\n'%(level*_INDENT, self._address())
        
        return _str

    def _address(self):
        if len(self.address) == 4:
            return socket.inet_ntoa(self.address)

class MDNSServiceRecord(MDNSResourceRecord):
    
    def __init__(self, name, recordType, recordClass, ttl, priority, weight, port, target):
        resourceDataLength = len(target) + PRIOR_WEIGHT_PORT_LEN
        MDNSResourceRecord.__init__(self, name, recordType, recordClass, ttl, resourceDataLength)
        
        self.priority = priority
        self.weight = weight
        self.port = port
        self.target = target

    def write(self, out):
        out.writeUnsignedShort(self.priority)
        out.writeUnsignedShort(self.weight)
        out.writeUnsignedShort(self.port)
        out.writeName(self.target)

    def __repr__(self, level=1):
        _str = ''
        _str += MDNSResourceRecord.__repr__(self, level)

        level += 1
        _str += '%sName: %s\n'%(level*_INDENT, self.name)
        _str += '%sPriority: %s\n'%(level*_INDENT, self.priority)
        _str += '%sWeight: %s\n'%(level*_INDENT, self.weight)
        _str += '%sPort: %s\n'%(level*_INDENT, self.port)
        _str += '%sTarget: %s\n'%(level*_INDENT, self.target)
        
        return _str

class MDNSPointerRecord(MDNSResourceRecord):
    
    def __init__(self, name, recordType, recordClass, ttl, resourceDataLength, service):
        MDNSResourceRecord.__init__(self, name, recordType, recordClass, ttl, resourceDataLength)
        
        self.service = service

    def __repr__(self, level=1):
        _str = ''
        _str += MDNSResourceRecord.__repr__(self, level)
        level += 1
        _str += '%sName: %s\n'%(level*_INDENT, self.service)
        
        return _str

class MDNSTextRecord(MDNSResourceRecord):
    
    def __init__(self, name, recordType, recordClass, ttl, text):
        resourceDataLength = len(text)
        MDNSResourceRecord.__init__(self, name, recordType, recordClass, ttl, resourceDataLength)

        self.text = text
        try:
            self.properties = self._textToProperties()
        except:
            self.properties = properties

    def write(self, out):
        out.write_string(self.text, len(self.text))

    def _propertiesToText(self):
        pass

    def _textToProperties(self):
        properties = {}
        index = 0
        end = len(self.text)
        while index < end:
            length = ord(self.text[index])
            index += 1
            property = self.text[index:index+length]
            index += length
            
            split = property.find('=')
            properties[property[:split]] = property[split + 1:] 
            
        return properties

    def __repr__(self, level=1):
        _str = ''
        _str += MDNSResourceRecord.__repr__(self, level)
        level += 1
        for key in self.properties.iterkeys():            
            _str += '%sText: %s=%s\n'%(level*_INDENT, key, self.properties[key])

        return _str

class MDNSOutgoingPacket(object):
    
    def __init__(self, flags):
        self.flags = flags
        self.identification = 0        
        self.data = []

        self.names = {}
        self.size = 12
        
        self.queries = []
        self.answers = []
        self.authorities = []
        self.additionals = []

    def addQuery(self, query):
        self.queries.append(query)

    def addAnswer(self, answer):
        self.answers.append(answer)

    def addAuthority(self, authority):
        self.authorities.append(authority)

    def addAdditional(self, additional):
        self.additionals.append(additional)

    def insertShort(self, index, value):
        format = '!H'
        self.data.insert(index, struct.pack(format, value))
        self.size += 2

    def writeQuery(self, query):
        self.writeName(query.name)
        self.writeUnsignedShort(query.type)
        self.writeUnsignedShort(query.clazz)

    def writeRecord(self, record):
        self.writeName(record.name)
        self.writeUnsignedShort(record.type)
        self.writeUnsignedShort(record.clazz)
        self.writeInteger(record.ttl)
        index = len(self.data)
        self.size += 2
        record.write(self)
        self.size -= 2
        length = len(''.join(self.data[index:]))
        self.insertShort(index, length)
        
    def writeName(self, name):
        if self.names.has_key(name):
            index = self.names[name]
            self.writeByte( (index >> 8) | 0xC0 )
            self.writeByte(index)            
        else:
            self.names[name] = self.size
            parts = name.split('.')
            if parts[-1] == '':
                parts = parts[:-1]
            for part in parts:
                self.writeUtf8(part)
            self.writeByte(0)
            
    def writeByte(self, value):
        format = '!c'
        self.data.append(struct.pack(format, chr(value)))
        self.size += 1

    def writeUtf8(self, str):
        utfstr = str.encode('utf-8')
        length = len(utfstr)
        self.writeByte(length)
        self.writeString(utfstr, length)
        
    def writeString(self, string, length):
        format = '!%ds'%length
        self.data.append(struct.pack(format, string))
        self.size += length 

    def writeUnsignedShort(self, value):
        format = '!H'
        length = struct.calcsize(format)
        data = struct.pack(format, value)
        self.data.append(data)
        self.size += 2

    def writeInteger(self, value):
        format = '!i'
        data = struct.pack(format, value)
        self.data.append(data)
        self.size += 4

    def packet(self):
        for query in self.queries:
            self.writeQuery(query)
        for answer in self.answers:
            self.writeRecord(answer)
        for authority in self.authorities:
            self.writeRecord(authority)
        for additional in self.additionals:
            self.writeRecord(additional)

        self.insertShort(0, len(self.additionals))
        self.insertShort(0, len(self.authorities))
        self.insertShort(0, len(self.answers))
        self.insertShort(0, len(self.queries))
        self.insertShort(0, self.flags)
        self.insertShort(0, self.identification)
        
        return ''.join(self.data)

class MDNSIncomingPacket(object):
    
    def __init__(self, packet):
        self.packet = packet
        self.offset = 0
        self.num_questions = 0
        self.num_answers = 0
        self.num_authorities = 0
        self.num_additionals = 0

        self.queryRecords = []
        self.answerRecords = []
        self.authorityRecords = []
        self.additionalRecords = []
        
        self.readHeader()
        self.readQueries()
        self.readAnswers()
        self.readAuthorities()
        self.readAdditionals()

    def __str__(self):
        level = 1
        _str = '\n'
        _str += '%sTransaction ID: 0x%.4x\n'%(level*_INDENT, self.identification)
        _str += '%sFlags: 0x%.4x\n'%(level*_INDENT, self.flags)
        _str += self.dump_flags(level+1)
        _str += '%sQuestions: %d\n'%(level*_INDENT, self.num_questions)        
        _str += '%sAnswer RRs: %d\n'%(level*_INDENT, self.num_answers)
        _str += '%sAuthority RRs: %d\n'%(level*_INDENT, self.num_authorities)
        _str += '%sAdditional RRs: %d\n'%(level*_INDENT, self.num_additionals)
        if self.num_questions > 0:
            _str += '%sQueries\n'%(level*_INDENT)
            _str += self.dump_queries(level+1)
        if self.num_answers > 0:
            _str += '%sAnswers\n'%(level*_INDENT)
            _str += self.dump_answers(level+1)
        if self.num_authorities > 0:
            _str += '%sAuthoritative nameservers\n'%(level*_INDENT)
            _str += self.dump_authorities(level+1)
        if self.num_additionals > 0:
            _str += '%sAdditional records\n'%(level*_INDENT)
            _str += self.dump_additionals(level+1)
        
        return _str

    def dump_flags(self, level):
        _str = ''
        if self.isQuery():
            _str += '%s0... .... .... .... = Response: Message is a query\n'%(level*_INDENT)
        else:
            _str += '%s1... .... .... .... = Response: Message is a response\n'%(level*_INDENT)

        opcode = (self.flags & _FLAGS_OPCODE_MASK) >> 11
        if opcode == STANDARD_QUERY:
            _str += '%s.000 0... .... .... = Opcode: Standard query (0)\n'%(level*_INDENT)
        elif opcode == INVERSE_QUERY:
            _str += '%s.000 1... .... .... = Opcode: Inverse query (1)\n'%(level*_INDENT)
        else:
            _str += '%s.000 2... .... .... = Opcode: Server status query (2)\n'%(level*_INDENT)
        
        return _str

    def dump_queries(self, level):
        _str = ''
        for query in self.queryRecords:
            _str += '%s%s'%(level*_INDENT, query)

        return _str

    def dump_answers(self, level):
        _str = ''
        for answer in self.answerRecords:
            _str += answer.__repr__(level)

        return _str

    def dump_authorities(self, level):
        _str = ''
        for authority in self.authorityRecords:
            _str += authority.__repr__(level)

        return _str

    def dump_additionals(self, level):
        _str = ''
        for additional in self.additionalRecords:
            _str += additional.__repr__(level)

        return _str

    def isQuery(self):
        qr = self.flags & _FLAGS_QR_MASK
        if qr == _FLAGS_QR_QUERY:
            return True
        else:
            return False

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
        
    def readQueries(self):
        format = '!HH'
        length = struct.calcsize(format)
        for i in range(0, self.num_questions):
            queryName = self.readName()
            query = struct.unpack(format, self.packet[self.offset:self.offset + length])
            self.offset += length
            
            self.queryRecords.append(MDNSQueryRecord(queryName, query[0], query[1]))

    def readAnswers(self):
        for domainName, answerRecord in self.readResourceRecords(self.num_answers):
            if answerRecord[0] == _TYPE_PTR:
                name = self.readName()
                self.answerRecords.append(MDNSPointerRecord(domainName, answerRecord[0], 
                                                            answerRecord[1], answerRecord[2], 
                                                            answerRecord[3], name))
            elif answerRecord[0] == _TYPE_TXT:
                text = self.readString(answerRecord[3])
                self.answerRecords.append(MDNSTextRecord(domainName, answerRecord[0],
                                                            answerRecord[1], answerRecord[2], 
                                                            text))
            elif answerRecord[0] == _TYPE_SRV:
                priority = self.readUnsignedShort()
                weight = self.readUnsignedShort()
                port = self.readUnsignedShort()
                target = self.readName()
                self.answerRecords.append(MDNSServiceRecord(domainName, answerRecord[0],
                                                            answerRecord[1], answerRecord[2], 
                                                            priority, weight, 
                                                            port, target))
            elif answerRecord[0] == _TYPE_A:
                address = self.readString(4)
                self.answerRecords.append(MDNSAddressRecord(domainName, answerRecord[0],
                                                            answerRecord[1], answerRecord[2], 
                                                            answerRecord[3], address))
            else:
                # ignore other types
                pass
    
    def readAuthorities(self):
        for domainName, authorityRecord in self.readResourceRecords(self.num_authorities):
            if authorityRecord[0] == _TYPE_PTR:
                name = self.readName()
                self.authorityRecords.append(MDNSPointerRecord(domainName, authorityRecord[0], 
                                                               authorityRecord[1], authorityRecord[2], 
                                                               authorityRecord[3], name))
            elif authorityRecord[0] == _TYPE_TXT:
                text = self.readString(answerRecord[3])
                self.authorityRecords.append(MDNSTextRecord(domainName, authorityRecord[0],
                                                            authorityRecord[1], authorityRecord[2], 
                                                            text))
            elif authorityRecord[0] == _TYPE_SRV:
                priority = self.readUnsignedShort()
                weight = self.readUnsignedShort()
                port = self.readUnsignedShort()
                target = self.readName()
                self.authorityRecords.append(MDNSServiceRecord(domainName, authorityRecord[0],
                                                               authorityRecord[1], authorityRecord[2], 
                                                               priority, weight, 
                                                               port, target))
            elif authorityRecord[0] == _TYPE_A:
                address = self.readString(4)
                self.authorityRecords.append(MDNSAddressRecord(domainName, authorityRecord[0],
                                                               authorityRecord[1], authorityRecord[2], 
                                                               authorityRecord[3], address))
            else:
                # ignore other types
                pass
    
    def readAdditionals(self):
        for domainName, additionalRecord in self.readResourceRecords(self.num_additionals):
            if additionalRecord[0] == _TYPE_PTR:
                name = self.readName()
                self.additionalRecords.append(MDNSPointerRecord(domainName, additionalRecord[0], 
                                                                additionalRecord[1], additionalRecord[2], 
                                                                additionalRecord[3], name))
            elif additionalRecord[0] == _TYPE_TXT:
                text = self.readString(additionalRecord[3])
                self.additionalRecords.append(MDNSTextRecord(domainName, additionalRecord[0],
                                                             additionalRecord[1], additionalRecord[2], 
                                                             text))
            elif additionalRecord[0] == _TYPE_SRV:
                priority = self.readUnsignedShort()
                weight = self.readUnsignedShort()
                port = self.readUnsignedShort()
                target = self.readName()
                self.additionalRecords.append(MDNSServiceRecord(domainName, additionalRecord[0],
                                                                additionalRecord[1], 
                                                                additionalRecord[2], priority, 
                                                                weight, port, target))
            elif additionalRecord[0] == _TYPE_A:
                address = self.readString(4)
                self.additionalRecords.append(MDNSAddressRecord(domainName, additionalRecord[0],
                                                                additionalRecord[1], additionalRecord[2], 
                                                                additionalRecord[3], address))
            else:
                # ignore other types
                pass

    def readResourceRecords(self, records):
        format = '!HHiH'
        length = struct.calcsize(format)
        for i in range(records):
            domainName = self.readName()
            resourceRecord = struct.unpack(format, self.packet[self.offset:self.offset + length])
            self.offset += length
            
            yield domainName, resourceRecord
                    
    def readName(self):
        compression = False
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
                next = offset + 1
                offset = (length & 0x3F) << 8 | ord(self.packet[offset])
            else:
                raise Exception('Bad name at position: %d'%offset)

        if next > 0:
            self.offset = next
        else:
            self.offset = offset
            
        return name

    def readInteger(self):
        format = '!i'
        length = struct.calcsize(format)
        data = struct.unpack(format, self.packet[self.offset:self.offset + length])
        self.offset += length
        
        return data[0]

    def readUnsignedShort(self):
        format = '!H'
        length = struct.calcsize(format)
        data = struct.unpack(format, self.packet[self.offset:self.offset + length])
        self.offset += length
        
        return data[0]

    def readString(self, length):
        format = '!%ds'%length
        length = struct.calcsize(format)
        data = struct.unpack(format, self.packet[self.offset:self.offset + length])
        self.offset += length

        return data[0]
