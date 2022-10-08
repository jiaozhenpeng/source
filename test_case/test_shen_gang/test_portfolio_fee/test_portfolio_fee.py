import unittest

from config import PathConfig
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import creat_new_dbf


class PortfolioFee(unittest.TestCase):
    """
    深港\证券组合费
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_gang())['PortfolioFee']

    def test_portfolio_fee(self):
        """
        深港\证券组合费
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深港\证券组合费 准备数据')
        dbf_path = self.yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('深港\证券组合费 数据准备完成')
            assert True
        else:
            logger().error('dbf文件数据准备异常，：{}'.format(dbf_result))
            assert False, dbf_result


if __name__ == '__main__':
    unittest.main()
