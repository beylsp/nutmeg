from bonjour.application import Application
from bonjour.mdns import _TYPE_SRV, _TYPE_A
from rtunes_service import RemoteTunesService
from web_service import PairFactory
from web_client import RemoteTunesClient

from twisted.internet import reactor

class RemoteTunesApplication(Application):

    browsable = '_touch-able._tcp.local'
    server = ''
    port = ''
    state = 'INIT'

    def __init__(self, name='ABCDEF1234567891'):
        Application.__init__(self)
        d = self.serviceBrowser.addService(self.browsable)
        d.addCallback(self.onDiscovered)

        self.rtservice = RemoteTunesService('%s._touch-remote._tcp.local'%name)
        self.serviceAdvertiser.addService(self.rtservice)

    def start(self):
        reactor.listenTCP(self.rtservice.getPort(), PairFactory(self.rtservice.getGuid(), 
                                                                self.rtservice.getDeviceName(), 
                                                                self.rtservice.getDeviceType(),
                                                                self.startShell))

        Application.start(self)

    def onDiscovered(self, packet):
        for record in packet.additionalRecords + packet.answerRecords:
            if record.getType() == _TYPE_SRV:
                self.port = record.getPort()
                target = record.getTarget()
                break
        for record in packet.additionalRecords + packet.answerRecords:
            if record.getType() == _TYPE_A and record.getName() == target:
                self.server = record.getAddress()
                break
        self.startShell()

    def startShell(self):
        if self.state == 'INIT':
            self.state = 'WAITING'
        elif self.state == 'WAITING':
            self.state = 'READY'
            RemoteTunesClient(self.rtservice.getGuid(), self.server, self.port)
