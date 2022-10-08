import os
import shutil
from datetime import datetime
from public_method import dbf_operation
import dbf
import cx_Oracle

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction


class DbfOperation():
    """
    读写dbf文件
    """
    t = OracleDatabase().get_trade_date()
    t1 = OracleDatabase().get_trade_date(1)
    t2 = OracleDatabase().get_trade_date(2)

    def __init__(self, path):
        self.dbf_file = dbf.Table(path, codepage='cp936')

    def creat_dbf(self, records, filename):
        """
        传入需要导入的数据列表和新文件名称，生成新的dbf文件
        :param records:
        :param filename:
        :return: bool
        """
        filename = filename + '.dbf'
        dbf_config = BaseAction().read_yaml(path=PathConfig().dbf())
        path = os.path.join(dbf_config['savePath'], self.t)
        if os.path.exists(path) is False:
            os.mkdir(path)
            logger().info('创建路径：{}'.format(path))
        file_path = os.path.join(dbf_config['getPath'], filename)
        new_file_path = os.path.join(path, filename)
        if os.path.exists(new_file_path) is False:
            shutil.copy(file_path, new_file_path)
            logger().info('新文件生成，生成路径：{}'.format(new_file_path))
        table = dbf.Table(new_file_path).open(mode=dbf.READ_WRITE)
        try:
            for record in records:
                if '_NULLFLAGS' in record:
                    del record['_NULLFLAGS']
                    logger().info('删除字段：_NULLFLAGS ')
                table.append(record)
            logger().info('文件数据添加成功:{}'.format(filename))
            table.close()
            return True
        except Exception as e:
            logger().info('文件数据添加失败:{}，错误信息{}'.format(filename, e))
            return False

    def delete_record(self):
        """
        清除dbf文件数据
        :return:
        """
        self.dbf_file.open(mode=dbf.READ_WRITE)
        while True:
            if not self.dbf_file:  # 判断是否有数据，没有数据结束循环
                break
            dbf.delete(self.dbf_file[0])
            self.dbf_file.pack()
        self.dbf_file.close()

    def get_data(self, **kwargs):
        """
        修改部分字段，字典格式传入对应的修改字段和修改后字段值，并返回修改后的文件数据列表
        :param kwargs:
        :return: [{},...]
        """
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                for key in kwargs.keys():
                    # logger().info('修改字段{}，修改前是:{},修改后为：{}'.format(key, rec[key], kwargs[key]))
                    rec[key] = kwargs[key]
            records.append(record)
        table.close()
        return records


def creat_new_dbf(path):
    """
    传路径，操作路径下所有dbf文件，修改日期并放至当前交易日期目录下
    :param path:
    :return:
    """
    dbf_names = BaseAction().get_dbf(path)
    dbf_result = []
    if not dbf_names:
        logger().error('当前路径下未找到dbf文件{}'.format(path))
        dbf_result.append('当前路径下未找到dbf文件{}'.format(path))
        return dbf_result
    for dbf_file in dbf_names:
        dbf_file_path = os.path.join(path, dbf_file)
        new_init = DbfOperation(dbf_file_path)
        func_name = dbf_file.replace('.dbf', '') + '_file'
        if hasattr(new_init, func_name):  # 判断方法是否存在
            new_dbf = getattr(new_init, func_name)
            new_dbf_result = new_init.creat_dbf(new_dbf(), dbf_file.replace('.dbf', ''))
            if new_dbf_result is False:
                dbf_result.append('{}创建失败'.format(dbf_file))
        else:
            logger().error('{} 未找到对应方法，请补充'.format(dbf_file))
            dbf_result.append('{} 未找到对应方法，请补充'.format(dbf_file))
    return dbf_result


if __name__ == '__main__':
    cur = cx_Oracle.connect('cts_kaifa','cts_kaifa').cursor()
    cur.execute(r'select stkid from stkinfo where exchid = {} '.format("'1'"))
    result=[]
    for i in cur.fetchall():
        dbf_file = DbfOperation(r'C:\Users\admin\Desktop\sjsdvpjg.dbf')
        zqdm = str(i[0])
        m=dbf_file.get_data(JGZQDM=zqdm)
        dbf_file.creat_dbf(m, 'sjsdvpjg')
    #     # print(a)
    #     result.append(dbf_file)
    # # for m in result:
    #     print(m)
    # dbf_file.creat_dbf(result,'sjsdvpjg')


    # dbf_record = dbf_file.bjsjg_file()
    # dbf_file.creat_dbf(dbf_record,'bjsjg')
    # d = creat_new_dbf('F:\source\用例数据\深权\普通开仓\准备昨持仓数据\\')
    # print(d)

