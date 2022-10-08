import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


class FreezeDay(unittest.TestCase):
    '''
    市场B\冻结变更和冻结结息\冻结日
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().market_b())
    def test_freeze(self):
        '''
        测试市场B\冻结变更和冻结结息\冻结日
        :return:
        '''
        logger().info('------------------')
        logger().info('开始执行 市场B\冻结变更和冻结结息\冻结日 准备数据')
        test_yaml = FreezeDay().yaml['FreezeDay']
        dbfPath = test_yaml['dbfPath']
        dbfPath1 = test_yaml['dbfPath1']
        sqlPath = test_yaml['sqlPath']
        dbf = DbfOperation(dbfPath)  # 初始化dbf
        dbf1 = DbfOperation(dbfPath1)
        oracle = OracleDatabase()  # 初始化oracle
        records = dbf.sjsgb_file()  # 获取原有dbf文件数据并修改日期
        records1 = dbf1.sjsjg_file()
        sql = BaseAction().read_sql(sqlPath)  # 获取执行的sql
        dbf_result = dbf.creat_dbf(records, 'sjsgb')
        dbf1_result = dbf1.creat_dbf(records1,'sjsjg')
        if dbf_result is False or dbf1_result is False:
            assert False, 'dbf文件新建失败'
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('市场B\冻结变更和冻结结息\冻结日 准备数据完成')
            assert True
        else:
            logger().error('市场B\冻结变更和冻结结息\冻结日 准备数据失败')
            assert False, oracle_result

    if __name__ == '__main__':
        unittest.main()