from mdns import MDNSOutgoingPacket, MDNSQueryRecord
from mdns import _FLAGS_QR_QUERY, _CLASS_IN, _TYPE_PTR
from mdns import MDNSIncomingPacket
from mdns import _TYPE_SRV, _TYPE_TXT

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log

import sys
log.startLogging(sys.stdout)

class ServiceBrowser(object):
    
    def __init__(self, zeroconf):        
        self.services = []
        self.discoverer = zeroconf
        self.discoverer.callback = self.update
        self.loopbrowse = LoopingCall(self.browse)
        reactor.callWhenRunning(self.browse)
        self.loopbrowse.start(2, False)
        
    def addService(self, service):
        if not self.services.__contains__(service):
            self.services.append(service)
        
    def removeService(self, service):
        if self.services.__contains__(service):
            self.services.remove(value)
    
    def browse(self):
        mdnsOut = MDNSOutgoingPacket(_FLAGS_QR_QUERY)
        for service in self.services:
            mdnsOut.addQuery(MDNSQueryRecord(service, _TYPE_PTR, _CLASS_IN))
        
        self.discoverer.sendDatagram(mdnsOut.packet())

    def update(self, packet):
        if not packet.isQuery():
            for answer in packet.answerRecords:
                if answer.getType() == _TYPE_SRV and (answer.getDomainName() in self.services):
                    print answer.name
                if answer.getType() == _TYPE_TXT and (answer.getDomainName() in self.services):
                    print answer.name
        
