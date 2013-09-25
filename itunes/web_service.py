from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

from media.dacp import TLV

class PairProtocol(Protocol):

    def __init__(self, guid, name, type, cb):        
        self.cb = cb        
        self.values = { 'cmpg': guid,
                        'cmnm': name,
                        'cmty': type
                      }

    def dataReceived(self, data):
        self.transport.write(self.answer())
        self.cb()

    def answer(self):
        values = []    
        for tag, value in self.values.iteritems():
            values.append(TLV(tag, value).tostring())            
        tlv = TLV('cmpa', values).tostring()
        
        http = 'HTTP/1.1 200 OK\r\n'
        http += 'Content-Length: %d\r\n\r\n'%len(tlv)
        http += tlv
        
        return http

class PairFactory(Factory):
    
    def __init__(self, guid, name, type, cb):
        self.guid = guid
        self.name = name
        self.type = type
        self.cb = cb

    def buildProtocol(self, address):
        return PairProtocol(self.guid, self.name, self.type, self.cb)