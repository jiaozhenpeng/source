import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastCustodyRegistration(unittest.TestCase):
    """
    对比 股转\托管登记
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['CustodyRegistration']

    def test_custody_registration(self):
        """
        对比 股转\托管登记
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 股转\托管登记 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' and" \
                         "  stkid = '810007' and briefid = '005_003_002'".format(year, begintime, endtime)
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID = 'GZ11721600' and stkid = '810007' and DESKID = 'ANQ001'"
        sktlistextend_sql = "select * FROM stklistextend  where exchid='6' and stkid = '810007' and DESKID ='ANQ001' " \
                            "and REGID = 'GZ11721600'"
        exchangerights_sql = "select * FROM exchangerights  where exchid='6' and stkid = '810007' and DESKID ='ANQ001'" \
                             " and REGID = 'GZ11721600'"
        stkauditingerror_sql = " select * from stkauditingerror where exchid='6' and businessdate={} and offerregid " \
                               "='GZ11721600' and stkid = '810007'".format(begintime)
        # 查询数据库
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        sktlistextend_database = base.stklistextend_sort(oracle.dict_data(sktlistextend_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        stkauditingerror_database = base.stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))
        # 查询excel
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        sktlistextend_excel = base.stklistextend_sort(excel.read_excel('sktlistextend'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        stkauditingerror_excel = base.stkauditingerror_sort(excel.read_excel('stkauditingerror'))
        # 排序
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        stklist_ignore = ()
        sktlistextend_ignore = ()
        exchangerights_ignore = ('RECKONINGTIME', 'KNOCKTIME')
        stkauditingerror_ignore = ('OCCURTIME', 'KNOCKTIME', 'BUSINESSDATE')
        # 对比数据
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        sktlistextend_result = base.compare_dict(sktlistextend_database, sktlistextend_excel, 'sktlistextend')
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights',
                                                  *exchangerights_ignore)
        stkauditingerror_result = base.compare_dict(stkauditingerror_database, stkauditingerror_excel,
                                                    'stkauditingerror', *stkauditingerror_ignore)
        # 断言
        final_result = tradinglog_result + stklist_result + sktlistextend_result + exchangerights_result + stkauditingerror_result
        if not final_result:
            logger().info('股转\托管登记 数据对比无异常')
            assert True
        else:
            logger().error('股转\托管登记 数据对比异常:{}'.format(final_result))
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
