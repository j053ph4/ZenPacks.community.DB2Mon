################################################################################
#
# This program is part of the DB2Mon Zenpack for Zenoss.
# Copyright (C) 2012 Joseph Anderson
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from ZenPacks.community.RDBMS.Database import Database

DOT_GREEN    = 'green'
DOT_PURPLE   = 'purple'
DOT_BLUE     = 'blue'
DOT_YELLOW   = 'yellow'
DOT_ORANGE   = 'orange'
DOT_RED      = 'red'
DOT_GREY     = 'grey'

SEV_CLEAR    = 0
SEV_DEBUG    = 1
SEV_INFO     = 2
SEV_WARNING  = 3
SEV_ERROR    = 4
SEV_CRITICAL = 5


class DB2Database(Database):
    """
    DB2 Database object
    """

    ZENPACKID = 'ZenPacks.community.DB2Mon'

    statusmap ={0: (DOT_GREEN, SEV_CLEAR, 'NORMAL'),
                1: (DOT_BLUE, SEV_INFO, 'LOAD PENDING'),
                2: (DOT_BLUE, SEV_INFO, 'LOAD IN PROGRESS'),
                3: (DOT_BLUE, SEV_INFO, 'REORG IN PROGRESS'),
                4: (DOT_YELLOW, SEV_WARNING, 'RESTORE IN PROGRESS'),
                5: (DOT_BLUE, SEV_INFO, 'TABLE SPACE DELETION IN PROGRESS'),
                6: (DOT_BLUE, SEV_INFO, 'TABLE SPACE CREATION IN PROGRESS'),
                7: (DOT_BLUE, SEV_INFO, 'BACKUP IN PROGRESS'),
                8: (DOT_BLUE, SEV_INFO, 'DMS REBALANCE IN PROGRESS'),
                9: (DOT_BLUE, SEV_INFO, 'BACKUP PENDING'),
                10: (DOT_YELLOW, SEV_WARNING, 'RESTORE PENDING'),
                11: (DOT_BLUE, SEV_INFO, 'ROLL FORWARD PENDING'),
                12: (DOT_BLUE, SEV_INFO, 'ROLL FORWARD IN PROGRESS'),
                13: (DOT_BLUE, SEV_INFO, 'QUIESCED EXCLUSIVE'),
                14: (DOT_BLUE, SEV_INFO, 'QUIESCED SHARE'),
                15: (DOT_BLUE, SEV_INFO, 'QUIESCED UPDATE'),
                16: (DOT_YELLOW, SEV_WARNING, 'STORAGE MAY BE DEFINED'),
                17: (DOT_YELLOW, SEV_WARNING, 'STORAGE MUST BE DEFINED'),
                18: (DOT_YELLOW, SEV_WARNING, 'DISABLE PENDING'),
                19: (DOT_YELLOW, SEV_WARNING, 'DROP PENDING'),
                20: (DOT_ORANGE, SEV_ERROR, 'SUSPEND WRITE'),
                21: (DOT_ORANGE, SEV_ERROR, 'UNAVAILABLE'),
                22: (DOT_RED, SEV_CRITICAL, 'OFFLINE AND NOT ACCESSIBLE'),
                }
                
                
    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('sizeUsed_totalBytes', 0)

    def dsn(self):
        """
        Return the DSN string
        """
        inst = self.getDBSrvInst()
        return getattr(inst, 'dsn', '')


InitializeClass(DB2Database)
