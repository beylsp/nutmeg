class Service(object):
    
    def __init__(self, name, port, target, ttl=120, priority=0, weight=0):
        self.name = name
        self.ttl = 120
        self.priority = priority
        self.weight = weight
        self.port = port 
        self.target = target
        self.text = {}

    def addText(self, key, value):
        self.text[key] = value

    def getText(self):
        return self.text
        
    def getName(self):
        return self.name

    def getPort(self):
        return self.port
    
    def getTarget(self):
        return self.target
    
    def getTtl(self):
        return self.ttl

    def getPriority(self):
        return self.priority

    def getWeight(self):
        return self.weight
