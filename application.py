from bonjour.zeroconfig import ZeroConfig
from bonjour.service_browser import ServiceBrowser
from bonjour.service_advertiser import ServiceAdvertiser
from bonjour.service import Service
from bonjour import MDNS_MULTICAST_PORT

from http import web_service

from twisted.internet import reactor
from twisted.web.server import Site

import socket

from twisted.python import log
import sys
log.startLogging(sys.stdout)

class Application(object):
    
    def __init__(self):
        self.zeroconf = ZeroConfig()
        self.serviceBrowser = ServiceBrowser(self.zeroconf)
        self.serviceAdvertiser = ServiceAdvertiser(self.zeroconf)

    def start(self):
        reactor.listenMulticast(MDNS_MULTICAST_PORT, self.zeroconf, listenMultiple=True)

        site = Site(web_service.getRoot(self.service))
        reactor.listenTCP(port, site)

        reactor.run()

    def createService(self, name, port, target):
        self.service.setName(name)
        self.service.setPort(port)
        self.service.setTarget(target)
        
        return self.service

class RemoteTunes(Application):
    
    def __init__(self, name='ABCDEF1234567890'):
        Application.__init__(self)
        
        self.serviceName = '%s._touch-remote._tcp.local'%name
        self.port = 6679
        self.target = socket.gethostname()
        self.ttl


    def start(self):        
        self.remote = self.createService() 



        self.serviceName = 
        self.ttl = 120
        self.priority = 0
        self.weight = 0
        self.port = 0
        self.target = ''
        self.properties = {}
        self.guid = ''
        
        
        self.itunes = Service()
