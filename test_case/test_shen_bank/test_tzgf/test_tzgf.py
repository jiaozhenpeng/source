import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


class Tzgf(unittest.TestCase):
    '''
    场景 深银行\互联互通数据 9位代码\TZGF
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())  # 获取yaml文件

    def test_tzgf(self):
        '''
        深银行\互联互通数据 9位代码\TZGF
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深银行\互联互通数据 9位代码\TZGF 数据准备')
        test_yaml = Tzgf().yaml['tzgf']
        dbf_path = test_yaml['dbfPath']  # 获取dbf文件路径
        dbf_path1 = test_yaml['dbfPath1']
        dbf = DbfOperation(dbf_path)  # 初始化dbf
        dbf1 = DbfOperation(dbf_path1)
        oracle = OracleDatabase()  # 初始化oracle
        records = dbf.szyh_sjsjg_file() # 获取原有dbf文件数据并修改日期
        records1 = dbf1.szyh_sjsjg_file()
        sql_path = test_yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        dbf_result = dbf.creat_dbf(records, 'szyh_sjsjg')  # 创建新的dbf文件
        dbf1_result = dbf1.creat_dbf(records1,'szyh_sjsjg')
        if dbf_result is False or dbf1_result is False: # 写入dbf文件错误时返回FALSE
            assert False, '文件新建失败'
        oracle_result = oracle.update_sql(*sql) # 全部执行成功返回空列表，否则返回错误sql
        if not oracle_result:
            logger().info('深银行\互联互通数据 9位代码\TZGF 数据准备完成')
            assert True
        else:
            logger().error('深银行\互联互通数据 9位代码\TZGF  数据准备失败')
            assert False,oracle_result

if __name__ == '__main__':
    unittest.main()



