import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation


class StockIndexOption(unittest.TestCase):
    """
    F市场\股指期权行权
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['MarketF']['IOexer1']

    def test_stock_index_option(self):
        """
        F市场\股指期权行权
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：F市场\股指期权行权 准备数据')
        txt_path1 = self.yaml['txtPath']
        txt_path2 = self.yaml['txtPath2']
        sql_path = self.yaml['sqlPath']
        txt1 = TxtOperation(txt_path1)
        txt2 = TxtOperation(txt_path2)
        oracle = OracleDatabase()
        # 创建文件
        txt_result1 = txt1.creat_txt('optexerdata')
        if txt_result1 is False:
            logger().error('optexerdata.txt文件创建失败')
            assert False, 'optexerdata.txt文件创建失败'
        txt_result2 = txt2.creat_txt('opttrddata')
        if txt_result2 is False:
            logger().error('opttrddata.txt文件创建失败')
            assert False, 'opttrddata.txt文件创建失败'
        # 执行SQL
        sql = BaseAction().read_sql(sql_path)
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('F市场\股指期权行权 准备数据完成')
            assert True
        else:
            logger().error('F市场\股指期权行权 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()