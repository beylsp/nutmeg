from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.defer import Deferred 
from twisted.internet import reactor

class RemoteTunesRequest(object):
    
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def new(self, uri):
        http = 'GET /%s HTTP/1.1\r\n'%uri
        http+= 'Host: %s:%d\r\n'%(self.server, self.port)
        http+= 'User-Agent: Remote/338\r\n'
        http+= 'Accept-Encoding: gzip\r\n'
        http+= 'Viewer-Only-Client: 1\r\n'
        http+= 'Client-Daap-Version: 3.11\r\n'
        http+= 'Accept: */*\r\n'
        http+= 'Accept-Language: nl-nl\r\n'
        http+= 'Connection: keep-alive\r\n'
        http+= '\r\n'
        
        return http

class RemoteTunesProtocol(Protocol):

    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        self.transport.loseConnection()
        
class RemoteTunesFactory(Factory):

    def buildProtocol(self, address):
        return RemoteTunesProtocol()

class RemoteTunesClient(object):
    
    def __init__(self, guid, server, port):
        self.guid = guid
        self.request = RemoteTunesRequest(server, port) 
        self.endpoint = TCP4ClientEndpoint(reactor, server, port)
        d = self.connect()
        d.addCallback(self.login)

    def connect(self):
        return self.endpoint.connect(RemoteTunesFactory())

    def login(self, protocol):
        request = self.request.new('login?pairing-guid=0x%s&hasFP=1'%self.guid.encode('hex'))
        protocol.sendMessage(request)

    def shell(self):
        pass
