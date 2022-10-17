import cx_Oracle
import os
import shutil


conn = cx_Oracle.connect('ctsdb', 'ctsdb', '192.168.4.1/ctsdb')
cursor = conn.cursor()
sql = 'SELECT tradedate FROM sysconfig'
cursor.execute(sql)
date = cursor.fetchone()[0]  #取当前交易日
newfiledate = str(date)[0:8]

path = r'C:\Users\admin\Desktop\20220928\T1_Huarun'
path2 = r'F:\开放式基金\import'

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
            final = a.replace('20220928',newfiledate)

        with open(filepath2,'w') as f:
            f.write(final)



