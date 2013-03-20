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
from ZenPacks.community.RDBMS.DBSrvInst import DBSrvInst

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

class DB2SrvInst(DBSrvInst):
    """
    DB2 SrvInst object
    """

    ZENPACKID = 'ZenPacks.community.DB2Mon'

    statusmap ={0: (DOT_GREEN, SEV_CLEAR, 'ACTIVE'),
                1: (DOT_YELLOW, SEV_WARNING, 'QUIESCE_PEND'),
                2: (DOT_ORANGE, SEV_ERROR, 'QUIESCED'),
                3: (DOT_YELLOW, SEV_WARNING, 'ROLLFWD'),
                4: (DOT_RED, SEV_CRITICAL, 'UNAVAILABLE'),
                }
                

    dsn = ''

    _properties = DBSrvInst._properties + (
        {'id':'dsn', 'type':'string', 'mode':'w'},
        )


InitializeClass(DB2SrvInst)
