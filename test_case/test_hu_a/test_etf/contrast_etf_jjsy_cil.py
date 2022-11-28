import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    货币ETF基金收益，cil文件
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['etfjjsy']['cil']

    def test_restricted_shares(self):
        """
        货币ETF基金收益，cil文件
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：货币ETF基金收益，cil文件 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from  stklist where exchid='0' and offerregid in('A117212000') " \
                      "and stkid in('517080','510410', '511860', '511990', '511980')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid  in('517080','510410', '511860', '511990', '511980')" \
                         "  and  briefid in('005_002_012','005_005_062')".format(year, begintime, endtime)

        # 获取数据库数据并排序

        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # 获取excel数据并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))

        # 可以忽略的字段
        stklist_ignore = ()
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME',
                             'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        # 对比数据
        stklist_result = BaseAction().compare_dict(stklist_database,stklist_excel,'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)

        final_result = tradinglog_result + stklist_result

        # 断言
        if not final_result :
            logger().info('货币ETF基金收益，cil文件 对比数据无异常')
            assert True
        else:
            logger().error('货币ETF基金收益，cil文件 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()