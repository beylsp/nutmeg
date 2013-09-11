from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from bonjour import MDNS_MULTICAST_ADDR, MDNS_MULTICAST_PORT
from mdns import MDNSIncomingPacket

class ServiceDiscovery(DatagramProtocol):
    
    def startProtocol(self):
        self.transport.joinGroup(MDNS_MULTICAST_ADDR)
        
    def datagramReceived(self, datagram, address):
        print datagram.encode('hex')
        mdnsIn = MDNSIncomingPacket(datagram)

        
reactor.listenMulticast(MDNS_MULTICAST_PORT, ServiceDiscovery())
reactor.run()