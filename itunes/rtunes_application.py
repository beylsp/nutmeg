from bonjour.application import Application
from bonjour.mdns import _TYPE_SRV, _TYPE_A
from rtunes_service import RemoteTunesService
from web_service import PairPage
from web_client import RemoteTunesClient
from bonjour import utils

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

class RemoteTunesApplication(Application):

    browsable = '_touch-able._tcp.local'

    def __init__(self, name='ABCDEF1234567890'):
        Application.__init__(self)
        d = self.serviceBrowser.addService(self.browsable)
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

    def onDiscovered(self, (serviceName, packet) ):
        for record in packet.additionalRecords:
            if record.getType() == _TYPE_SRV:
                port = record.getPort()
                target = record.getTarget()
            elif record.getType() == _TYPE_A and record.getName() == target:
                server = record.getAddress()
        RemoteTunesClient(self.rtservice.getGuid(), server, port)
