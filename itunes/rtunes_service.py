from bonjour.service import Service

import socket

class RemoteTunesService(Service):
    
    def __init__(self, name):
        Service.__init__(self)
        
        self.setTtl(120)
        self.setPriority(0)
        self.setWeight(0)
        self.setPort(7966)
        self.setName(name)
        self.setTarget(socket.gethostname())

        

    def setGuid(self, guid):
        self.guid = guid
        
    def getGuid(self):
        return self.guid

    def setDeviceName(self, name):
        self.addProperty('DvNm', name)

    def setRemoteVersion(self, version):
        self.addProperty('RemV', version)

    service.addProperty('RemV', '10000')
    service.addProperty('DvTy', 'iPod Touch')
    service.addProperty('RemN', 'Remote')
    service.addProperty('Pair', '09CF644AC278442F')
    service.addProperty('txtvers', '1')    
