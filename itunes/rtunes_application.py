from bonjour.application import Application
from rtunes_service import RemoteTunesService

class RemoteTunesApplication(Application):
    
    def __init__(self, name='ABCDEF1234567890'):
        Application.__init__(self)
        
        self.rtunes = RemoteTunesService('%s._touch-remote._tcp.local'%name)

    def start(self):        
        self.remote = self.createService()
