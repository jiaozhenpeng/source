import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastInfiniteLimit(unittest.TestCase):
    """
    对比 股转\无限售流通股份转限售
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['InfiniteLimit']

    def test_infinite_limit(self):
        """
        股转\无限售流通股份转限售
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转\无限售流通股份转限售 对比数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        base = BaseAction()
        endtime = begintime[0:8] + '235959'
        year = base.get_today_date()[:4]
        # 对比SQL
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID ='GZ11721600' and STKID ='839106' and " \
                      "DESKID = 'ANQ001'"
        stklistextend_sql = "select * FROM stklistextend  where exchid='6' and stkid ='839106' and DESKID ='ANQ001' " \
                            "and REGID ='GZ11721600'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' and  " \
                         "stkid ='839106' and briefid in('005_003_043','005_004_002') and REGID ='GZ11721600'".format(
            year, begintime, endtime)
        exchangerights_sql = "select * FROM exchangerights  where exchid='6' and stkid = '839106' and DESKID ='ANQ001'" \
                             " and REGID = 'GZ11721600'"
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        # excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        # 忽略字段
        stklist_ignore = ()
        stklistextend_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        exchangerights_ignore = ()
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextend_result = base.compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog_', *tradinglog_ignore)
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        # 断言
        final_result = stklist_result + stklistextend_result + tradinglog_result + exchangerights_result
        if not final_result:
            logger().info('股转\无限售流通股份转限售数据对比无异常')
            assert True
        else:
            logger().error('股转\无限售流通股份转限售 数据对比异常:{}'.format(final_result))
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
