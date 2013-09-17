from bonjour.service_browser import ServiceBrowser
from bonjour.service_advertiser import ServiceAdvertiser
from bonjour.service import Service

from twisted.internet import reactor

if __name__ == '__main__':
    serviceBrowser = ServiceBrowser()
    serviceBrowser.addService('_touch-able._tcp_local.')

    serviceAdvertiser = ServiceAdvertiser()
    service = Service('ABCDEF1234567890._touch-remote._tcp.local.', 51186, 'device.local')
    service.addText('DvNm', 'device')
    service.addText('RemV', '10000')
    service.addText('DvTy', 'iPod Touch')
    service.addText('RemN', 'Remote')
    service.addText('Pair', '09CF644AC278442F')
    service.addText('txtvers', '1')    
    serviceAdvertiser.addService(service)

    reactor.run()
