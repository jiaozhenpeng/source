

import unittest
from config import PathConfig
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


class ThawingDay(unittest.TestCase):

    '''
    市场B\冻结变更和冻结结息\解冻日
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().market_b())

    def test_thawing_day(self):
        '''
        准备数据：市场B\冻结变更和冻结结息\解冻日
        :return:
        '''
        logger().info('------------------')
        logger().info('开始执行  市场B\冻结变更和冻结结息\解冻日 准备数据')
        test_yaml = ThawingDay().yaml['ThawingDay']
        dbfPath = test_yaml['dbfPath']
        dbf = DbfOperation(dbfPath)  # 初始化dbf
        records = dbf.sjsjg_file()  # 获取原有dbf文件数据并修改日期
        dbf_result = dbf.creat_dbf(records, 'sjsjg')
        if dbf_result is False:
            assert False, '文件新建失败'
        else:
            assert True
        # sqlPath =
        # oracle = OracleDatabase()  # 初始化oracle
        # sql = BaseAction().read_sql(sqlPath)  # 获取执行的sql
        # oracle_result = oracle.update_sql(*sql)
        # if not oracle_result:
        #     logger().info('市场B\冻结变更和冻结结息\解冻日 准备数据完成')
        #     assert True
        # else:
        #     logger().error('市场B\冻结变更和冻结结息\解冻日 准备数据失败')
        #     assert False, oracle_result

if __name__ == '__main__':
    unittest.main()

