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
        self.setTarget('%s.local'%socket.gethostname())        

        self.setGuid('00000001')
        self.setDeviceName(socket.gethostname())
        self.setRemoteVersion('10000')
        self.setDeviceType('iPod Touch')
        self.setRemoteName('MyRemote')
        self.setPair('09CF644AC278442F')
        self.setTxtVersion('1')

    def setGuid(self, guid):
        self.guid = guid
        
    def getGuid(self):
        return self.guid

    def setDeviceName(self, name):
        self.addProperty('DvNm', name)

    def getDeviceName(self):
        return self.getProperty('DvNm')

    def setRemoteVersion(self, version):
        self.addProperty('RemV', version)

    def getRemoteVersion(self):
        return self.getProperty('RemV')

    def setDeviceType(self, type):
        self.addProperty('DvTy', type)

    def getDeviceType(self):
        return self.getProperty('DvTy')
        
    def setRemoteName(self, name):
        self.addProperty('RemN', name)

    def getRemoteName(self):
        return self.getProperty('RemN')
        
    def setPair(self, pair):
        self.addProperty('Pair', pair)

    def getPair(self):
        return self.getProperty('Pair')
        
    def setTxtVersion(self, version):
        self.addProperty('txtvers', version)

    def getTextVersion(self):
        return self.getProperty('txtvers')
