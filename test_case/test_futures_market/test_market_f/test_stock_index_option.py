import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation


class StockIndexOption(unittest.TestCase):
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
        logger().info('开始执行：F市场\股指期权 准备数据')
        txt_path = self.yaml['txtPath']
        txt = TxtOperation(txt_path)
        # 创建文件
        txt_result = txt.creat_txt('opttrddata')
        if txt_result is False:
            logger().error('opttrddata.txt文件创建失败')
            assert False, 'opttrddata.txt文件创建失败'
        sql_path = self.yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        oracle = OracleDatabase()
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('F市场\股指期权 准备数据完成')
            assert True
        else:
            logger().error('F市场\股指期权 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()