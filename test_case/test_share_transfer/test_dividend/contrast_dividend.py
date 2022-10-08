import unittest

from config import PathConfig
from log.logger import logger
from public_method.base_action import BaseAction


class ContrastDividend(unittest.TestCase):
    """
    对比 股转\分红派息
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['Dividend']

    def test_dividend(self):
        """
        对比 股转\分红派息
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比  股转\QFII股份对账 数据')
        excel_path = self.yaml['excelPath']
        pass