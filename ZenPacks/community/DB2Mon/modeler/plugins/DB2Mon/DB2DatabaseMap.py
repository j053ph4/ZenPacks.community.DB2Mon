################################################################################
#
# This program is part of the DB2Mon Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DB2DatabaseMap.py

DB2DatabaseMap maps the DB2 Databases table to Database objects

$Id: DB2DatabaseMap.py,v 1.7 2012/04/26 22:59:16 egor Exp $"""

__version__ = "$Revision: 1.7 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
import re

DBSTATES = {
          'ACTIVE':0,
          'QUIESCE_PEND':1,
          'QUIESCED':2,
          'ROLLFWD':3,
          'UNAVAILABLE':4,
          }

STATES = {'NORMAL':0,
        'LOAD PENDING':1,
        'LOAD IN PROGRESS':2,
        'REORG IN PROGRESS':3,
        'RESTORE IN PROGRESS':4,
        'TABLE SPACE DELETION IN PROGRESS':5,
        'TABLE SPACE CREATION IN PROGRESS':6,
        'TABLE SPACE CREATION IN PROGRESS':7,
        'BACKUP IN PROGRESS':8,
        'DMS REBALANCE IN PROGRESS':9,
        'BACKUP PENDING':10, # RECOVERY
        'RESTORE PENDING':11,
        'ROLL FORWARD PENDING':12,
        'ROLL FORWARD IN PROGRESS':13,
        'QUIESCED EXCLUSIVE':14,
        'QUIESCED SHARE':15,
        'QUIESCED UPDATE':16,
        'STORAGE MAY BE DEFINED':17,
        'STORAGE MUST BE DEFINED':18,
        'DISABLE PENDING':19,
        'DROP PENDING':20,
        'SUSPEND WRITE':21,
        'UNAVAILABLE':22,
        'OFFLINE AND NOT ACCESSIBLE':23,
        }

class DB2DatabaseMap(ZenPackPersistence, SQLPlugin):


    ZENPACKID = 'ZenPacks.community.DB2Mon'

    maptype = "DatabaseMap"
    compname = "os"
    relname = "softwaredbsrvinstances"
    modname = "ZenPacks.community.DB2Mon.DB2SrvInst"
    deviceProperties = SQLPlugin.deviceProperties + ('zDB2Username',
                                                    'zDB2Password',
                                                    'zDB2ConnectionString',
                                                    'zDB2DSN',
                                                    'zDB2TablespaceIgnoreNames',
                                                    'zDB2TablespaceIgnoreTypes',
                                                    )

    def queries(self, device):
        
        tasks = {}
        connectionString = getattr(device, 'zDB2ConnectionString', '') or \
            "'ibm_db_dbi','${here/dsn}','${here/zDB2Username}','${here/zDB2Password}'"
        dsns = getattr(device, 'zDB2DSN', '') or \
            "'DATABASE=DBNAME;HOSTNAME=${here/manageIp};PORT=50000;PROTOCOL=TCPIP'"
        if type(dsns) is str:
            dsns = [dsns]
        for inst, dsn in enumerate(dsns):
            if not dsn.strip(): continue
            setattr(device, 'dsn', self.prepareCS(device, dsn))
            cs = self.prepareCS(device, connectionString)
            tasks['si_%s'%inst] = (
                "SELECT DB_NAME, DB_STATUS, SERVER_PLATFORM FROM SYSIBMADM.SNAPDB",
                None,
                cs,
                {
                    'dbsiname':'DB_NAME',
                    'status': 'DB_STATUS',
                    'dsn':dsn,
                })
            tasks['st_%s'%inst] = (
                "SELECT INST_NAME, SERVICE_LEVEL FROM SYSIBMADM.ENV_INST_INFO",
                None,
                cs,
                {
                    'instance': 'INST_NAME',
                    'setProductKey':'SERVICE_LEVEL',
                })
             
            tasks['db_%s'%inst] = (
                """SELECT TBSP_ID, TBSP_NAME, TBSP_TYPE, 
                 TBSP_TOTAL_PAGES , TBSP_PAGE_SIZE,
                 TBSP_STATE
                 FROM SYSIBMADM.TBSP_UTILIZATION""",
                None,
                cs,
                {
                    'dbid':'TBSP_ID',
                    'dbname':'TBSP_NAME',
                    'type':'TBSP_TYPE',
                    'blockSize':'TBSP_PAGE_SIZE',
                    'totalBlocks':'TBSP_TOTAL_PAGES',
                    'setDBSrvInst':'instance',
                    'status':'TBSP_STATE',
                })
        return tasks

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        skiptsnames = getattr(device, 'zDB2TablespaceIgnoreNames', None)
        skiptstypes = getattr(device, 'zDB2TablespaceIgnoreTypes', None)
        maps = [self.relMap()]
        dsns = getattr(device, 'zDB2DSN', '') or \
            "'DATABASE=DBNAME;HOSTNAME=${here/manageIp};PORT=50000;PROTOCOL=TCPIP'"
        databases = []
        for tname, instances in results.iteritems():
            if tname.startswith('si_'):
                for i,inst in enumerate(instances):
                    dbindex = int(tname[3:])
                    om = self.objectMap(inst)
                    om.id = self.prepId(om.dbsiname)
                    om.dsn = self.prepareCS(device, dsns[dbindex])
                    print "DSN",om.dsn,dbindex
                    try:
                        prodkey = results.get('st_%s'%dbindex) [0]['setProductKey']
                        om.setProductKey = MultiArgs(prodkey, 'IBM')
                    except:
                        pass
                    om.status = DBSTATES.get(getattr(om, 'status', ''), 1)
                    maps[-1].append(om)
            elif tname.startswith('st_'): continue
            else: 
                for info in instances:
                    dbindex = tname[3:]
                    dbname = results.get('si_%s'%dbindex)[0]['dbsiname']
                    info['setDBSrvInst'] = dbname
                databases.extend(instances)
        self.relname = "softwaredatabases"
        self.modname = "ZenPacks.community.DB2Mon.DB2Database"
        maps.append(self.relMap())
        for tspace in databases:
            if (skiptsnames and re.search(skiptsnames,tspace['dbname'])):continue
            if (skiptstypes and re.search(skiptstypes,tspace['type'])):continue
            try:
                om = self.objectMap(tspace)
                om.id = self.prepId('%s_%s'%(om.setDBSrvInst, om.dbname))
                om.status = STATES.get(getattr(om, 'status', ''), 6)
            except AttributeError:
                continue
            maps[-1].append(om)
        return maps


