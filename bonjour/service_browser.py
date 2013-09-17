from mdns import MDNSOutgoingPacket, MDNSQueryRecord
from mdns import _FLAGS_QR_QUERY, _CLASS_IN, _TYPE_PTR
from mdns import MDNSIncomingPacket
from service_discovery import ServiceDiscovery
from bonjour import MDNS_MULTICAST_PORT

from twisted.internet import reactor
from twisted.python import log

import sys
log.startLogging(sys.stdout)

class ServiceBrowser(object):
    
    def __init__(self):        
        self.services = []
        self.discoverer = ServiceDiscovery()
        self.discoverer.callback = self.update
        reactor.listenMulticast(MDNS_MULTICAST_PORT, self.discoverer, listenMultiple=True)
        reactor.callWhenRunning(self.browse)
        
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

    def update(self, datagram):
        pass
