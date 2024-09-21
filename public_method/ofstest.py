import cx_Oracle
import os
import shutil
import datetime
import dbf
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction



conn = cx_Oracle.connect('ctsdb', 'ctsdbj', '173.168.64.238/ctsdb')
cursor = conn.cursor()
sql = 'SELECT tradedate FROM sysconfig'
cursor.execute(sql)
date = cursor.fetchone()[0]  #取当前交易日
newfiledate = str(date)[0:8]

path = r'F:\source\用例数据\开放式基金\清算文件'
path2 = path2 = os.path.join('F:\测试生成数据',newfiledate,'开放式基金')

if os.path.exists(path2):
    shutil.rmtree(path2)
    os.mkdir(path2)


pathfiles = os.walk(path)
for root,dirs,files in pathfiles:
    for filename in files:
        filenamedate = str(filename)[11:19]
        newname = filename.replace(filenamedate,newfiledate)
        filepath = os.path.join(path,filename)
        filepath2 = os.path.join(path2, newname)
        print(filepath2)
        print(filepath)
        with open(filepath,'r') as f:
            a = f.read()
            final = a.replace('20220302',newfiledate)


        with open(filepath2,'w') as f:
            f.write(final)



