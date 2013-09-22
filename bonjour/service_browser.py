from mdns import MDNSOutgoingPacket, MDNSQueryRecord
from mdns import _FLAGS_QR_QUERY, _CLASS_IN, _TYPE_PTR
from mdns import MDNSIncomingPacket
from mdns import _TYPE_SRV, _TYPE_TXT

from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.task import LoopingCall

class ServiceBrowser(object):
    
    _STATE_SRV = 0
    _STATE_TXT = 0
    
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
        mdnsOut = MDNSOutgoingPacket(_FLAGS_QR_QUERY)
        mdnsOut.addQuery(MDNSQueryRecord(self.service, _TYPE_PTR, _CLASS_IN))
        
        self.discoverer.sendDatagram(mdnsOut.packet())

    def update(self, packet):
        if not packet.isQuery():
            for answer in packet.answerRecords:
                if answer.getType() == _TYPE_SRV and (answer.getDomainName() == self.service):
                    self._STATE_SRV = 1
                if answer.getType() == _TYPE_TXT and (answer.getDomainName() == self.service):
                    self._STATE_TXT = 1
            for answer in packet.additionalRecords:
                if answer.getType() == _TYPE_SRV and (answer.getDomainName() == self.service):
                    self._STATE_SRV = 1
                if answer.getType() == _TYPE_TXT and (answer.getDomainName() == self.service):
                    self._STATE_TXT = 1

        if self._STATE_SRV and self._STATE_TXT and self.defer is not None:
            d, self.defer = self.defer, None
            d.callback(packet)
