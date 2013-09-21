from application import Application

from twisted.internet import reactor

if __name__ == '__main__':
    name = 'myDevice'
    app = Application()
    app.serviceBrowser.addService('_touch-able._tcp_local')

    service = app.createService('ABCDEF1234567895._touch-remote._tcp.local', 51186, '%s.local'%name)
    service.setTtl(120)
    service.setGuid('00000001')
    service.addProperty('DvNm', name)
    service.addProperty('RemV', '10000')
    service.addProperty('DvTy', 'iPod Touch')
    service.addProperty('RemN', 'Remote')
    service.addProperty('Pair', '09CF644AC278442F')
    service.addProperty('txtvers', '1')    
    app.serviceAdvertiser.addService(service)

    app.start()