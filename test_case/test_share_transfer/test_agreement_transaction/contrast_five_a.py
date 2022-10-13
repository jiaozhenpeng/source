import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastFiveA(unittest.TestCase):
    """
    股转\协议交易\A5
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['AgreementTransaction']['fiveA']

    def test_five_a(self):
        """
        股转\协议交易\A5
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转\协议交易\A5 对比数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        # account_sql = "select * from ACCOUNT where ACCTID in ('000011721600','000011721601')and CURRENCYID='00'"
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID in( 'GZ11721601','GZ11721600') and STKID in " \
                      "('810003','810004') and DESKID = 'ANQ001'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' and " \
                         " stkid in ('810003','810004') and briefid in('005_002_001','005_001_001')".format(year,
                                                                                                            begintime,
                                                                                                            endtime)
        # todaytraderslt_sql = "select * from TODAYTRADERSLT where STKID in ('810003','810004') and DESKID = 'ANQ001' and" \
        #                      " EXCHID = '6' and reckoningtime>={} and reckoningtime<={}".format(begintime, endtime)
        # finalreckoningresult_sql = "select * from finalreckoningresult where EXCHID='6' and DESKID = 'ANQ001' and STKID " \
        #                            "in ('810003','810004') and REGID in ('GZ11721600','GZ11721601') and ACCTID in " \
        #                            "('000011721600','000011721601')"
        stkauditingerror_sql = " select * from stkauditingerror where exchid='6' and businessdate={} and offerregid =" \
                               "'GZ11721600' and stkid in ('810003','810004')".format(begintime)
        # 数据库数据
        # account_database = base.account_sort(oracle.dict_data(account_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # todaytraderslt_database = base.todaytraderslt_sort(oracle.dict_data(todaytraderslt_sql))
        # finalreckoningresult_database = base.finalreckoningresult_sort(oracle.dict_data(finalreckoningresult_sql))
        stkauditingerror_database = base.stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))
        # excel数据
        # account_excel = base.account_sort(excel.read_excel('account'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # todaytraderslt_excel = base.todaytraderslt_sort(excel.read_excel('todaytraderslt'))
        # finalreckoningresult_excel = base.finalreckoningresult_sort(excel.read_excel('finalreckoningresult'))
        stkauditingerror_excel = base.stkauditingerror_sort(excel.read_excel('STKAUDITINGERROR'))
        # 忽略字段
        account_ignore = ()
        stklist_ignore = ()
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        # todaytraderslt_ignore = ('RECKONINGTIME', 'KNOCKTIME', 'SERIALNUM')
        finalreckoningresult_ignore = ()
        stkauditingerror_ignore = ('OCCURTIME', 'KNOCKTIME', 'BUSINESSDATE')
        # 对比
        # account_result = base.compare_dict(account_database, account_excel, 'account')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)

        stkauditingerror_result = base.compare_dict(stkauditingerror_database, stkauditingerror_excel,
                                                    'stkauditingerror', *stkauditingerror_ignore)
        # 断言
        final_result =  stklist_result + tradinglog_result  #/*+ stkauditingerror_result*/
        if not final_result:
            logger().info('股转\协议交易\A5 数据对比无异常')
            assert True
        else:
            logger().error('股转\协议交易\A5 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()