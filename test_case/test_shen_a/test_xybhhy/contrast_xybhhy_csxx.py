import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    深A\信用保护合约\CSXX现金结算
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['XYBHHY']['CSXX']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_restricted_shares(self):
        """
        深A\信用保护合约\CSXX现金结算
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\信用保护合约\CSXX现金结算 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid='1' and " \
                         "briefid in('005_005_083','005_005_084')".format(year,begintime,endtime)
        # 获取数据库数据并排序

        tradinglog_database = BaseAction().tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 获取excel数据并排序
        tradinglog_excel = BaseAction().tradinglog_sort(excel.read_excel('tradinglog'))
        # 可以忽略的字段
        tradinglog_ignore= self.ignore['tradinglog']
        # 对比数据

        tradinglog_result = BaseAction().compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)


        # 断言
        if not tradinglog_result :
            logger().info('深A\信用保护合约\CSXX现金结算 对比数据无异常')
            assert True
        else:
            logger().error('深A\信用保护合约\CSXX现金结算 对比数据异常')
            assert False, tradinglog_result


if __name__ == '__main__':
    unittest.main()