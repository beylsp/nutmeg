from twisted.web.resource import Resource

import struct

def getRoot(service):
    root = Resource()
    root.putChild('pair', PairPage(service.getGuid(), service.getProperty('DvNm'), service.getProperty('DvTy')))

    return root

class PairPage(Resource):

    def __init__(self, guid, name, type):
        self.guid = guid
        self.name = name
        self.type = type

    values = { 'cmpg': '\x00\x00\x00\x00\x00\x00\x00\x01',
               'cmnm': 'devicename',
               'cmty': 'ipod',
             }

    def answer(self):
        encoded = ''
        for key, value in self.values.iteritems():
            encoded += '%s%s%s' % (key, struct.pack('>i', len(value)), value)
        header = 'cmpa%s' % (struct.pack('>i', len(encoded)))
        encoded = '%s%s' % (header, encoded)
        
        return encoded

    def render_GET(self, request):
        print '%s %s'%(request.method, request.uri)
        return self.answer()

    def render_POST(self, request):
        self.render_GET(request)
