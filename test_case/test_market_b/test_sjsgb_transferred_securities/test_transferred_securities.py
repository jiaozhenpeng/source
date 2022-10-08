
import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation

class TransferredSecurities(unittest.TestCase):

    yaml = BaseAction().read_yaml(path=PathConfig().market_b())
    def test_transferred_securities(self):
        '''
        准备数据：市场B\sjsgb转入证券信息
        :return:
        '''
        logger().info('------------------')
        logger().info('开始执行市场B\sjsgb转入证券信息 准备数据')
        test_yaml = TransferredSecurities().yaml['TransferredSecurities']
        dbfPath1 = test_yaml['dbfPath1']
        sqlPath = test_yaml['sqlPath']
        dbf1 = DbfOperation(dbfPath1)  # 初始化dbf
        oracle = OracleDatabase()  # 初始化oracle
        records1 = dbf1.szyh_sjsgb_file()  # 获取原有dbf文件数据并修改日期
        sql = BaseAction().read_sql(sqlPath) # 获取执行的sql
        dbf1_result =  dbf1.creat_dbf(records1,'szyh_sjsgb')
        if  dbf1_result is False :
            assert False,'文件新建失败'
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('市场B\sjsgb转入证券信息 准备数据完成')
            assert True
        else:
            logger().error('市场B\sjsgb转入证券信息 准备数据失败')
            assert False,oracle_result
if __name__ == '__main__':
    unittest.main()