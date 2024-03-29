import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastFiveE(unittest.TestCase):
    """
    股转\协议交易\E5数据\协议交易
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['AgreementTransaction']['fiveE']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())
    def test_five_e(self):
        """
        股转\协议交易\E5数据\协议交易
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转\协议交易\E5数据\协议交易 准备数据')
        dbf_path = self.yaml['dbfPath']
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        # account_sql = "select * from ACCOUNT where ACCTID in ('000011721600','000011721601')and CURRENCYID='00'"
        stklist_sql = "select * from STKLIST where EXCHID = '9' and REGID in( 'GZ11721601','GZ11721600') and STKID in " \
                      "('810010','810011','810013') and DESKID = 'ANQ001'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '9' and " \
                         " stkid in ('810010','810011','810013','810012') and briefid in('005_002_001'," \
                         "'005_001_001')".format(year,begintime,endtime)

        stkauditingerror_sql = " select * from stkauditingerror where exchid='9' and businessdate={} and offerregid =" \
                               "'GZ11721600' and stkid in ('810010','810011','810013','810012')".format(begintime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stkauditingerror_database = base.stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))
        # excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        stkauditingerror_excel = base.stkauditingerror_sort(excel.read_excel('STKAUDITINGERROR'))
        # 忽略字段
        account_ignore = ()
        stklist_ignore = ()
        tradinglog_ignore = self.ignore['tradinglog']
        stkauditingerror_ignore = self.ignore['stkauditingerror']
        openorder_ignore =()
        # 对比
        # account_result = base.compare_dict(account_database, account_excel, 'account')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # todaytraderslt_result = base.compare_dict(todaytraderslt_database, todaytraderslt_excel,
        #                                           'todaytraderslt', *todaytraderslt_ignore)
        # finalreckoningresult_result = base.compare_dict(finalreckoningresult_database, finalreckoningresult_excel,
        #                                                 'finalreckoningresult')
        stkauditingerror_result = base.compare_dict(stkauditingerror_database, stkauditingerror_excel,
                                                    'stkauditingerror', *stkauditingerror_ignore)
        # openorder_result = base.compare_dict(openorder_database,openorder_excle,'openorder')
        # 断言
        final_result =  stklist_result + tradinglog_result  #+  stkauditingerror_result
        if not final_result:
            logger().info('股转\协议交易\E5 数据对比无异常')
            assert True
        else:
            logger().error('股转\协议交易\E5 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
