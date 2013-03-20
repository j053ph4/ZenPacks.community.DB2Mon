import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ DB2Mon loader
    """

    packZProperties = [
            ('zDB2ConnectionString', "'ibm_db_dbi','${here/dsn}','',''", 'string'),
            ('zDB2DSN', ['DATABASE=DBNAME;HOSTNAME=${here/manageIp};PORT=${here/tcpport};PROTOCOL=TCPIP;UID=${here/zDB2Username};PWD=${here/zDB2Password}'], 'lines'),
            ('zDB2Username', '', 'string'),
            ('zDB2Password', '', 'password'),
            ('zDB2TablespaceIgnoreNames', '', 'string'),
            ('zDB2TablespaceIgnoreTypes', '', 'string'),
            ]
