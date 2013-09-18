from application import Application

from twisted.internet import reactor

if __name__ == '__main__':
    app = Application()
    app.serviceBrowser.addService('_touch-able._tcp_local')

    service = app.createService('ABCDEF1234567892._touch-remote._tcp.local', 51186, 'myNewDevice.local')
    service.setTtl(0)
    service.addProperty('DvNm', 'my own device')
    service.addProperty('RemV', '10000')
    service.addProperty('DvTy', 'iPod Touch')
    service.addProperty('RemN', 'Remote')
    service.addProperty('Pair', '09CF644AC278442F')
    service.addProperty('txtvers', '1')    
    app.serviceAdvertiser.addService(service)

    reactor.run()
