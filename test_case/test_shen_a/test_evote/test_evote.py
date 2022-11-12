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
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['lofbuysell']

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




if __name__ == '__main__':
    unittest.main()