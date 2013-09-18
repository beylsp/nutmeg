import struct

def propertiesToText(properties):
    list = []
    text = ''
    for key in properties.keys():
        value = properties[key]
        if value == None:
            suffix = ''.encode('utf-8')
        elif isinstance(value, str):
            suffix = value.encode('utf-8')
        elif isinstance(value, int):
            if value:
                suffix = 'true'
            else:
                suffix = 'false'
        else:
            suffix = ''.encode('utf-8')
        list.append('='.join((key, suffix)))
    for item in list:
        text = ''.join( (text, struct.pack('!c', chr(len(item))), item) )

    return text

def textToProperties(text):
    properties = {}
    index = 0
    end = len(text)
    while index < end:
        length = ord(text[index])
        index += 1
        property = text[index:index+length]
        index += length
        
        split = property.find('=')
        properties[property[:split]] = property[split + 1:] 
        
    return properties
