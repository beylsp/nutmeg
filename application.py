from bonjour.zeroconfig import ZeroConfig
from bonjour.service_browser import ServiceBrowser
from bonjour.service_advertiser import ServiceAdvertiser
from bonjour.service import Service
from bonjour import MDNS_MULTICAST_PORT

from twisted.internet import reactor

class Application(object):
    
    def __init__(self):
        self.zeroconf = ZeroConfig()
        self.serviceBrowser = ServiceBrowser(self.zeroconf)
        self.serviceAdvertiser = ServiceAdvertiser(self.zeroconf)
        
        reactor.listenMulticast(MDNS_MULTICAST_PORT, self.zeroconf, listenMultiple=True)
        
    def createService(self, name, port, target):
        return Service(name, port, target)
                