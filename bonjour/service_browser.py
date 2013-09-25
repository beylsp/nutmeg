from mdns import MDNSOutgoingPacket, MDNSQueryRecord
from mdns import _FLAGS_QR_QUERY, _CLASS_IN, _TYPE_PTR
from mdns import MDNSIncomingPacket
from mdns import _TYPE_SRV, _TYPE_TXT

from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.task import LoopingCall

class ServiceBrowser(object):
    
    def __init__(self, zeroconf):        
        self.service = ''
        self.discoverer = zeroconf
        self.discoverer.callback = self.update
        self.loopbrowse = LoopingCall(self.browse)
        reactor.callWhenRunning(self.browse)
        self.loopbrowse.start(120, False)
        
    def addService(self, service):
        self.defer = defer.Deferred()
        self.service = service
        return self.defer
            
    def browse(self):
        self.query = MDNSQueryRecord(self.service, _TYPE_PTR, _CLASS_IN)
        mdnsOut = MDNSOutgoingPacket(_FLAGS_QR_QUERY)
        mdnsOut.addQuery(self.query)
        
        self.discoverer.sendDatagram(mdnsOut.packet())

    def update(self, packet):
        if packet.isResponse():            
            for answer in packet.answerRecords:
                if self.query.isAnsweredBy(answer) and self.defer is not None:
                    d, self.defer = self.defer, None
                    d.callback(packet)
