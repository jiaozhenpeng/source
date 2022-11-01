import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastStockIndexOption(unittest.TestCase):
    """
    F市场\股指期权
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['MarketF']['StockIndexOption']

    def test_stock_index_option(self):
        """
        F市场\股指期权
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：F市场\股指期权 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL




        if not final_result:
            logger().info('F市场\股指期权 对比数据无异常')
            assert True
        else:
            logger().error('F市场\股指期权 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    a = ContrastStockIndexOption.test_stock_index_option()