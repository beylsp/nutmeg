from twisted.web.resource import Resource

from media.dacp import TLV

class PairPage(Resource):

    def __init__(self, guid, name, type):
        self.values = { 'cmpg': guid,
                        'cmnm': name,
                        'cmty': type
                      }

    def answer(self):
        values = []    
        for tag, value in self.values.iteritems():
            values.append(TLV(tag, value).tostring())            
        return TLV('cmpa', values).tostring()

    def render_GET(self, request):
        return self.answer()

    def render_POST(self, request):
        self.render_GET(request)
