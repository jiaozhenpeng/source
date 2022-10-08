import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation

# 深A\股票买卖  测试用例


class TestStockTrading(unittest.TestCase):

    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())
    def test_stock_purchase(self):
        '''
        # 股票买卖\股票买入
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深A\股票买卖\股票买入')
        stock_purchase = TestStockTrading().yaml['stockPurchase']
        dbf_path = stock_purchase['stockPurchasePath'] # 获取股票买入dbf文件路径
        dbf = DbfOperation(dbf_path)
        oracle = OracleDatabase()
        records = dbf.sjsmx1_file()
        dbf.creat_dbf(records,'sjsmx1')
        sql_path = stock_purchase['sql']
        sql = BaseAction().read_sql(sql_path)
        try:
            oracle.update_sql(*sql)
            logger().info('深A\股票买卖\股票买入 数据准备完成')
            assert True
        except Exception as e:
            logger().error('深A\股票买卖\股票买入 数据准备失败')
            logger().error(e)
            assert False

    def test_virtual_shareholder_purchase(self):
        '''
        测试股票买入虚拟股东
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深A\股票买卖\股票买入虚拟股东')
        shareholder_purchase = TestStockTrading().yaml['shareholderPurchase']
        dbf_path = shareholder_purchase['shareholderPath']  # 获取股票买入dbf文件路径
        dbf = DbfOperation(dbf_path)
        oracle = OracleDatabase()
        records = dbf.sjsmx1_file()
        dbf.creat_dbf(records, 'sjsmx1')
        sql_path = shareholder_purchase['sql']
        sql = BaseAction().read_sql(sql_path)
        try:
            oracle.update_sql(*sql)
            logger().info('深A\股票买卖\股票买入虚拟股东 数据准备完成')
            assert True
        except Exception as e:
            logger().error('深A\股票买卖\股票买入虚拟股东 数据准备失败')
            logger().error(e)
            assert False


if __name__ == '__main__':
    unittest.main()



