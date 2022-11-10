import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import creat_new_dbf


class BlockTrade(unittest.TestCase):
    """
    沪A\上证lof\转托管转出\T1day
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['lofztgzc']['T1day']

    def test_block_trade(self):
        """
        沪A\上证lof\认购\T1day
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\上证lof\转托管转出\T1day 准备数据')
        dbf_path = self.yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('dbf文件数据准备完成')
        else:
            logger().error('dbf文件数据准备异常，：{}'.format(dbf_result))
            assert False, dbf_result

if __name__ == '__main__':
    unittest.main()