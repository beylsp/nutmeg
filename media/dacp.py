import struct

#1    char     1-byte value, can be used as a boolean (true if the value is present, false if not)
#3     short     2-byte integer
#5     long     4-byte integer
#7     long long     8-byte integer, tends to be represented in hex rather than numerical form
#9     string     string of characters (UTF-8)
#10     date     4-byte integer with seconds since 1970 (standard UNIX time format)
#11     version     2-bytes major version, next byte minor version, last byte patchlevel
#12     container     contains a series of other chunks, one after the other

TAGS = {
        'miid':    ('dmap.itemid',                  LONG),
        'minm':    ('dmap.itemname',                STRING),
        'mikd':    ('dmap.itemkind',                DLONG),
        'mper':    ('dmap.persistentid',            STRING),
        'mcon':    ('dmap.container',               CONTAINER),
        'mcti':    ('dmap.containeritemid',         LONG),
        'mpco':    ('dmap.parentcontainerid',       LONG),
        'mstt':    ('dmap.status',                  LONG),
        'msts':    ('dmap.statusstring',            STRING),
        'mimc':    ('dmap.itemcount',               LONG),
        'mctc':    ('dmap.containercount',          LONG),
        'mrco':    ('dmap.returnedcount',           LONG),
        'mtco':    ('dmap.specifiedtotalcount',     LONG),
        'f?ch':    ('dmap.haschildcontainers',      CHAR),
        'mlcl':    ('dmap.listing',                 CONTAINER),
        'mlit':    ('dmap.listingitem',             CONTAINER),
        'mbcl':    ('dmap.bag',                     CONTAINER),
        'mdcl':    ('dmap.dictionary',              CONTAINER),
        'msrv':    ('dmap.serverinforesponse',      CONTAINER),
        'msau':    ('dmap.authenticationmethod',    CHAR),
        'msas':    ('dmap.authenticationschemes',   LONG),
        'mslr':    ('dmap.loginrequired',           CHAR),
        'mpro':    ('dmap.protocolversion',         VERSION),
        'msal':    ('dmap.supportsautologout',      CHAR),
        'msup':    ('dmap.supportsupdate',          CHAR),
        'mspi':    ('dmap.supportspersistentids',   CHAR),
        'msex':    ('dmap.supportsextensions',      CHAR),
        'msbr':    ('dmap.supportsbrowse',          CHAR),
        'msqy':    ('dmap.supportsquery',           CHAR),
        'msix':    ('dmap.supportsindex',           CHAR),
        'msrs':    ('dmap.supportsresolve',         CHAR),
        'mstm':    ('dmap.timeoutinterval',         LONG),
        'msdc':    ('dmap.databasescount',          LONG),
        'mstc':    ('dmap.utctime',                 DATE),
        'msto':    ('dmap.utcoffset',               LONG),
        'mlog':    ('dmap.loginresponse',           CONTAINER),
        'mlid':    ('dmap.sessionid',               LONG),
        'mupd':    ('dmap.updateresponse',          CONTAINER),
        'musr':    ('dmap.serverrevision',          LONG),
        'muty':    ('dmap.updatetype',              CHAR),
        'mudl':    ('dmap.deletedid',               CONTAINER),
        'msdc':    ('dmap.databasescount',          LONG),
        'mccr':    ('dmap.contentcodesresponse',    CONTAINER),
        'mcnm':    ('dmap.contentcodesnumber',      LONG),
        'mcna':    ('dmap.contentcodesname',        STRING),
        'mcty':    ('dmap.contentcodestype',        SHORT),
        'meds':    ('dmap.editcommandssupported',   LONG)
       }

class TLV(object):
    
    def __init__(self, tag, value):
        if isinstance(value, list):
            value = ''.join(value)
    
        self.tlv = '%s%s%s'%(tag, struct.pack('>i', len(value)), value)

    def tostring(self):
        return self.tlv

class Parser(object):
    
    def __init__(self, tlv):
        self._tlv = tlv

    def __str__(self):
        pass

    def getValue(self, tag):
        pass
