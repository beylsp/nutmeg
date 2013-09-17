from bonjour import MDNS_MULTICAST_ADDR, MDNS_MULTICAST_PORT
from mdns import MDNSIncomingPacket

from twisted.internet.protocol import DatagramProtocol
from twisted.python import log

class ServiceDiscovery(DatagramProtocol):

    def startProtocol(self):
        self.transport.joinGroup(MDNS_MULTICAST_ADDR)

    def datagramReceived(self, datagram, address):
        log.msg('MDNS packet received from %s'%address[0])
        mdnsIn = MDNSIncomingPacket(datagram)
        log.msg(mdnsIn)
        
        if self.callback:
            self.callback(datagram)

    def sendDatagram(self, datagram):
        address = (MDNS_MULTICAST_ADDR, MDNS_MULTICAST_PORT)
        self.transport.write(datagram, address)
