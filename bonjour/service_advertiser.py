import utils
from mdns import MDNSOutgoingPacket, MDNSServiceRecord, MDNSTextRecord, MDNSPointerRecord, MDNSAddressRecord
from mdns import _FLAGS_QR_RESP, _CLASS_IN, _TYPE_SRV, _TYPE_TXT, _TYPE_PTR, _TYPE_A
from mdns import MDNSIncomingPacket

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.python import log

import sys
log.startLogging(sys.stdout)

class ServiceAdvertiser(object):
    
    def __init__(self, zeroconf):
        self.services = []
        self.advertiser = zeroconf
        self.loopadvert = LoopingCall(self.advertise)
        reactor.callWhenRunning(self.advertise)
        self.loopadvert.start(2, False)

    def addService(self, service):
        if not self.services.__contains__(service):
            self.services.append(service)
        
    def removeService(self, service):
        if self.services.__contains__(service):
            self.services.remove(value)
    
    def advertise(self):
        mdnsOut = MDNSOutgoingPacket(_FLAGS_QR_RESP)
        for service in self.services:
            mdnsOut.addAnswer(MDNSAddressRecord(service.getTarget(), _TYPE_A, _CLASS_IN,
                                                service.getTtl(), '192.168.1.2'))
            mdnsOut.addAnswer(MDNSPointerRecord(service.getDomainName(), _TYPE_PTR, _CLASS_IN,
                                                service.getTtl(), service.getName()))
            mdnsOut.addAnswer(MDNSServiceRecord(service.getName(), _TYPE_SRV, _CLASS_IN,
                                                service.getTtl(), service.getPriority(),
                                                service.getWeight(), service.getPort(),
                                                service.getTarget()))
            if len(service.properties) > 0:
                mdnsOut.addAnswer(MDNSTextRecord(service.getName(), _TYPE_TXT, _CLASS_IN,
                                                 service.getTtl(), 
                                                 utils.propertiesToText(service.getProperties())))
        
        self.advertiser.sendDatagram(mdnsOut.packet())
