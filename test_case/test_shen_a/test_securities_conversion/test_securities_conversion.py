import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation

class SecuritiesConversion(unittest.TestCase):

    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())

    def test_securities_conversion(self):
        '''
        测试 证券转换 数据准备
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深A\证券转换 数据准备')
        test_yaml = SecuritiesConversion().yaml['SecuritiesConversion']
        dbf_path = test_yaml['dbfPath']  # 获取股票买入dbf文件路径
        dbf = DbfOperation(dbf_path)
        oracle = OracleDatabase()
        records = dbf.sjsjg_file()
        dbf.creat_dbf(records, 'sjsjg')
        sql_path = test_yaml['sql']
        sql = BaseAction().read_sql(sql_path)
        try:
            oracle.update_sql(*sql)
            logger().info('深A\证券转换 数据准备完成')
            assert True
        except Exception as e:
            logger().error('深A\证券转换 数据准备失败')
            logger().error(e)
            assert False
if __name__ == '__main__':
    unittest.main()