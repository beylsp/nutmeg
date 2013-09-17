from mdns import MDNSOutgoingPacket, MDNSServiceRecord, MDNSTextRecord
from mdns import _FLAGS_QR_RESP, _CLASS_IN, _TYPE_SRV, _TYPE_TXT
from mdns import MDNSIncomingPacket
from service_discovery import ServiceDiscovery
from bonjour import MDNS_MULTICAST_PORT

from twisted.internet import reactor
from twisted.python import log

import sys
log.startLogging(sys.stdout)

class ServiceAdvertiser(object):
    
    def __init__(self):
        self.services = []
        self.advertiser = ServiceDiscovery()
        self.advertiser.callback = self.update
        reactor.listenMulticast(MDNS_MULTICAST_PORT, self.advertiser, listenMultiple=True)
        reactor.callWhenRunning(self.advertise)

    def addService(self, service):
        if not self.services.__contains__(service):
            self.services.append(service)
        
    def removeService(self, service):
        if self.services.__contains__(service):
            self.services.remove(value)
    
    def advertise(self):
        mdnsOut = MDNSOutgoingPacket(_FLAGS_QR_RESP)
        for service in self.services:
            mdnsOut.addAnswer(MDNSServiceRecord(service.getName(), _TYPE_SRV, _CLASS_IN,
                                                service.getTtl(), service.getPriority(),
                                                service.getWeight(), service.getPort(),
                                                service.getTarget()))
            if len(service.text) > 0:
                mdnsOut.addAnswer(MDNSTextRecord(service.getName(), _TYPE_TXT, _CLASS_IN,
                                                 service.getTtl(), service.getText()))
        
        self.advertiser.sendDatagram(mdnsOut.packet())

    def update(self, datagram):
        pass
