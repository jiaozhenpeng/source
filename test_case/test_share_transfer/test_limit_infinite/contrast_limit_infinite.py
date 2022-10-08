import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastLimitInfinite(unittest.TestCase):
    """
    股转\限售股份转无限售流通股
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['LimitInfinite']

    def test_limit_infinite(self):
        """
        股转\限售股份转无限售流通股
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转\限售股份转无限售流通股 对比数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        base = BaseAction()
        endtime = begintime[0:8] + '235959'
        year = base.get_today_date()[:4]
        # 对比SQL
        pass