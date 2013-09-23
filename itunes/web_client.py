from twisted.internet import reactor
from twisted.web.client import Agent

class RtunesRequest(object):
    
    def __init__(self, server, port):
        self.agent = Agent(reactor)

        self.server = server
        self.port = port

    def new(self, uri):
        return self.agent.request('GET', 'http://%s:%d/%s'%(self.server, self.port, uri), None, None)
        
class RemoteTunesClient(object):
    
    def __init__(self, guid, server, port):
        self.request = RtunesRequest(server, port)
        self.login(guid)

    def login(self, guid):
        d = self.request.new('login?pairing-guid=0x%s'%guid)
        d.addCallback(self.cbResponse)
        
    def cbResponse(self, response):
        print 'response received...'
        print response