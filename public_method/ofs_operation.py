import cx_Oracle
import os
import shutil
import datetime
import dbf
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from multiprocessing import Process

class OfsOperation():
    '''
    1111
    '''
    today = OracleDatabase().get_trade_date()
    lasttradedate1 = OracleDatabase().get_last_trade_date(1)
    print(today)
    def __init__(self):
        pass


    def copyfile(self):
        path = r'F:\source\用例数据\开放式基金\清算文件'
        path2 = os.path.join('F:\测试生成数据',self.today,'开放式基金')
        if os.path.exists(path2) is False:
            os.makedirs(path2)    #使用os.makedirs才能创建多级路径，os.makedir只能创建一级路径
            logger().info('创建路径：{}'.format(path))

        pathfiles = os.walk(path)
        for root, dirs, files in pathfiles:
            for filename in files:
                filenamedate = str(filename)[11:19]
                newname = filename.replace(filenamedate, self.today)
                filepath = os.path.join(path, filename)
                filepath2 = os.path.join(path2, newname)
                if os.path.exists(filepath2):
                    os.remove(filepath2)
                print(filepath2)
                print(filepath)
                if filename in ('OFI_99_678_20220302.TXT','OFI_98_678_20220302.TXT'):
                    with open(filepath, 'r') as f:
                        a = f.read()
                        final = a.replace('20220302', self.today)   #复制文件所有内容，替换掉日期
                    with open(filepath2, 'w') as f:
                        f.write(final)      #将复制的数据存入清算路径下
                elif filename in ('OFD_99_678_20220302_04.TXT','OFD_98_678_20220302_04.TXT'):
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                        line_to_modify = 4
                        lines[line_to_modify] = lines[line_to_modify].replace('20220302',self.today)







    def modifytime(self):
        path2 = os.path.join('F:\测试生成数据',self.today,'开放式基金')





if __name__ == '__main__':
    OfsOperation().copyfile()