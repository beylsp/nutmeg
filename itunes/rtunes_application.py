from bonjour.application import Application
from rtunes_service import RemoteTunesService
from web_service import PairPage

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

class RemoteTunesApplication(Application):

    def __init__(self, name='ABCDEF1234567890'):
        Application.__init__(self)
        d = self.serviceBrowser.addService('_touch-able._tcp.local')
        d.addCallback(self.onDiscovered)

        self.rtservice = RemoteTunesService('%s._touch-remote._tcp.local'%name)
        self.serviceAdvertiser.addService(self.rtservice)

        self.webroot = Resource()
        self.webroot.putChild('pair', PairPage(self.rtservice.getGuid(), 
                                               self.rtservice.getDeviceName(), 
                                               self.rtservice.getDeviceType()))

    def start(self):
        reactor.listenTCP(self.rtservice.getPort(), Site(self.webroot))

        Application.start(self)

    def onDiscovered(self, packet):
        print 'discovered...'
        print packet
