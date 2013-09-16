from datetime import datetime
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.defer import Deferred
from twisted.internet import reactor

from bonjour import MDNS_MULTICAST_ADDR, MDNS_MULTICAST_PORT
from mdns import MDNSIncomingPacket

class ServiceDiscovery(DatagramProtocol):

    def __init__(self):
        self.deferred = Deferred()
    
    def startProtocol(self):
        self.transport.joinGroup(MDNS_MULTICAST_ADDR)

        from service_browser import ServiceBrowser
        sb = ServiceBrowser()
        sb.addService('_touch-able._tcp_local.')
        m = sb.browse()
        self.sendDatagram(m)

    def datagramReceived(self, datagram, address):
        self.dprint('%s: MDNS packet received from %s'%(datetime.now().strftime('%H:%M:%S.%f'), address[0]))
        mdnsIn = MDNSIncomingPacket(datagram)
        self.dprint(mdnsIn)
#         if mdnsIn == self.service:
#             d, self.deferred = self.deferred, None 
#             d.callback(mdnsIn)

    def sendDatagram(self, datagram):
        address = (MDNS_MULTICAST_ADDR, MDNS_MULTICAST_PORT)
        self.dprint('%s: MDNS packet sent to %s:%s'%(datetime.now().strftime('%H:%M:%S.%f'), address[0], address[1]))
        
        from mdns import MDNSIncomingPacket
        print MDNSIncomingPacket(datagram)
        
        self.transport.write(datagram, address)

    def dprint(self, log):
        print log

def onServiceDiscovered(mdns):
    print 'service discovered...'

sd = ServiceDiscovery()
#sd.deferred.addCallback(onServiceDiscovered)
reactor.listenMulticast(MDNS_MULTICAST_PORT, sd, listenMultiple=True)
reactor.run()
