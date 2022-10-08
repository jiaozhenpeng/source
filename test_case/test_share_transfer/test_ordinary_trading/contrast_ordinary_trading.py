import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastOrdinaryTrading(unittest.TestCase):
    """
    对比 股转\普通买卖
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['OrdinaryTrading']

    def test_ordinary_trading(self):
        """
        对比 股转\普通买卖
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比  股转\普通买卖 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        year = BaseAction().get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID in( 'GZ11721600','GZ11721601') and STKID in" \
                      " ('830999','430089','430140') and DESKID = 'ANQ001'"
        finalreckoningresult_sql = "select * from finalreckoningresult where EXCHID='6' and DESKID = 'ANQ001' and STKID" \
                                   " in ('830999','430089','430140','831353') and REGID in ('GZ11721600','GZ11721601')" \
                                   " and ACCTID in ('000011721600','000011721601')"
        todaytraderslt_sql = "select * from TODAYTRADERSLT where STKID in ('830999','430089','430140','831353') and " \
                             "DESKID = 'ANQ001' and EXCHID = '6' and reckoningtime>={} and reckoningtime<={}".format(
            begintime, endtime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' and" \
                         "  stkid in ('830999','430089','430140','831353') and briefid in('005_001_001','005_002_001')".format(
            year, begintime, endtime)
        # 获取数据库数据并排序
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        finalreckoningresult_database = BaseAction().finalreckoningresult_sort(
            oracle.dict_data(finalreckoningresult_sql))
        todaytraderslt_database = BaseAction().todaytraderslt_sort(oracle.dict_data(todaytraderslt_sql))
        tradinglog_database = BaseAction().tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 获取excel数据并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        finalreckoningresult_excel = BaseAction().finalreckoningresult_sort(excel.read_excel('finalreckoningresult'))
        todaytraderslt_excel = BaseAction().todaytraderslt_sort(excel.read_excel('todaytraderslt'))
        tradinglog_excel = BaseAction().tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 忽略字段
        stklist_ignore = ()
        finalreckoningresult_ignore = ()
        todaytraderslt_ignore = ('RECKONINGTIME', 'KNOCKTIME', 'SERIALNUM')
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        # 对比数据
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        finalreckoningresult_result = BaseAction().compare_dict(finalreckoningresult_database,
                                                                finalreckoningresult_excel, 'finalreckoningresult')
        todaytraderslt_result = BaseAction().compare_dict(todaytraderslt_database, todaytraderslt_excel,
                                                          'todaytraderslt', *todaytraderslt_ignore)
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog',
                                                      *tradinglog_ignore)
        # 断言
        final_result = stklist_result + finalreckoningresult_result + todaytraderslt_result +tradinglog_result
        if not final_result:
            logger().info('股转\普通买卖 数据对比无异常')
            assert True
        else:
            logger().error('股转\普通买卖 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()

