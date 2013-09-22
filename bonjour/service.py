class Service(object):

    properties = {}
    
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name

    def getDomainName(self):
        index = self.name.find('.')
        return self.name[index+1:]
    
    def setPort(self, port):
        self.port = port
        
    def getPort(self):
        return self.port

    def setTarget(self, target):
        self.target = target
        
    def getTarget(self):
        return self.target
        
    def setTtl(self, ttl):
        self.ttl = ttl

    def getTtl(self):
        return self.ttl

    def setPriority(self, priority):
        self.priority = priority

    def getPriority(self):
        return self.priority
        
    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def addProperty(self, key, value):
        self.properties[key] = value

    def getProperties(self):
        return self.properties

    def getProperty(self, property):
        return self.properties[property]
