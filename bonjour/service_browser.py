from mdns import MDNSOutgoingPacket, MDNSQueryRecord
from mdns import _FLAGS_QR_QUERY, _CLASS_IN, _TYPE_PTR

class ServiceBrowser(object):
    
    def __init__(self):
        self.services = []
        
    def addService(self, service):
        if not self.services.__contains__(service):
            self.services.append(service)
        
    def removeService(self, service):
        if self.services.__contains__(service):
            self.services.remove(value)
    
    def browse(self):
        service = self.services.pop()
        mdnsOut = MDNSOutgoingPacket(_FLAGS_QR_QUERY)
        mdnsOut.addQuery(MDNSQueryRecord(service, _TYPE_PTR, _CLASS_IN))
        out = mdnsOut.packet()
        
        #from mdns import MDNSIncomingPacket
        #mdnsIn = MDNSIncomingPacket(out)
        #print mdnsIn

        return out
