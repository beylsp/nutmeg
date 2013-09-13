from datetime import datetime
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from bonjour import MDNS_MULTICAST_ADDR, MDNS_MULTICAST_PORT
from mdns import MDNSIncomingPacket

class ServiceDiscovery(DatagramProtocol):
    
    def startProtocol(self):
        self.transport.joinGroup(MDNS_MULTICAST_ADDR)
        
    def datagramReceived(self, datagram, address):
        print '%s: MDNS packet received from %s'%(datetime.now().strftime('%H:%M:%S.%f'), address[0])
        mdnsIn = MDNSIncomingPacket(datagram)
        self.dprint(mdnsIn)
        
    def dprint(self, mdnsIn):
        print mdnsIn
        
reactor.listenMulticast(MDNS_MULTICAST_PORT, ServiceDiscovery(), listenMultiple=True)
reactor.run()