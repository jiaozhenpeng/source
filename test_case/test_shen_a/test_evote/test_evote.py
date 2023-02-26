import unittest

import shutil
import os
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from config import PathConfig


class BlockTrade(unittest.TestCase):
    """
    深A\V5投票
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['Evote']

    def test_block_trade(self):
        """
        深A\V5投票
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\V5投票 准备数据')
        filepath = r'F:\source\用例数据\深A\V5投票\evotereport.csv'
        dbf_config = BaseAction().read_yaml(path=PathConfig().dbf())
        path = os.path.join(dbf_config['savePath'], OracleDatabase().get_trade_date())
        shutil.copy(filepath, path)
        sql_path = self.yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        oracle = OracleDatabase()
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('深A\V5投票 准备数据完成')
            assert True
        else:
            logger().error('深A\V5投票 准备数据异常')
            assert False, sql_result




if __name__ == '__main__':
    unittest.main()