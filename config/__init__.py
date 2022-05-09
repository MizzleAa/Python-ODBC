####################################################################################
# __init__
#
# 해당 위치에는 .json 및 xml과 같은 ip/port 정보 및
# 사용 알고리즘에 따른 부가 필요 정보를 가져온다.
####################################################################################
# __all__ = ['Decorator']

import json
from os import path
from lib.Logger import LogSystem

configPathDir = path.dirname(path.abspath(__file__))
with open(f'{configPathDir}/config.json', 'r') as jsonFile:
    configDict = json.load(jsonFile)

# Tibero
tiberoIP = str(configDict['tibero']['ip'])
tiberoPort = str(configDict['tibero']['port'])
tiberoDSN = str(configDict['tibero']['dsn'])
tiberoDatabase = str(configDict['tibero']['database'])
tiberoID = str(configDict['tibero']['id'])
tiberoPWD = str(configDict['tibero']['pwd'])

# Mssql
mssqlDriver = str(configDict['mssql']['driver'])
mssqlIP = str(configDict['mssql']['ip'])
mssqlPort = str(configDict['mssql']['port'])
mssqlDatabase = str(configDict['mssql']['database'])
mssqlUsername = str(configDict['mssql']['username'])
mssqlPassword = str(configDict['mssql']['password'])

logDir = str(configDict['Settings']['logDir'])
logName = str(configDict['Settings']['logName'])
loggerServerIP = str(configDict['Settings']['loggingIP'])
loggerServerPort = int(configDict['Settings']['loggingPort'])

groupName = str(configDict['Settings']['groupName'])

timeDELETE = str(configDict['time']['DELETE'])
timeKCS_ITEM_INFO = str(configDict['time']['KCS_ITEM_INFO'])
timeTB_AIX_MNG001M = str(configDict['time']['TB_AIX_MNG001M'])
timeTB_AIX_AI002M = str(configDict['time']['TB_AIX_AI002M'])
timeTB_AIX_MNT001M = str(configDict['time']['TB_AIX_MNT001M'])
timeTB_AIX_AI003M = str(configDict['time']['TB_AIX_AI003M'])

logSystem = LogSystem()
log = logSystem.socketLogger(loggerServerIP, loggerServerPort)
