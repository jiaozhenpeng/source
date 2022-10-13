import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastConsolidated(unittest.TestCase):
    """
    沪A/合并申报
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['Consolidated']

    def test_consolidated(self):
        """
        沪A/合并申报
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A/合并申报 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询sql
        # account_sql = "select * from ACCOUNT{} where ACCTID in ('000000301528','000011720300','000011739200')and " \
        #               "CURRENCYID='00' and OCCURTIME ={}".format(year,begintime)
        stklist_sql = "select * from STKLIST{} where EXCHID = '0' and REGID in( '0000301528','A117203000','A117392000') " \
                      "and STKID in ('020056','130291') and DESKID = '00W40' and OCCURTIME ={}".format(year,begintime)
        stklistcurrent_sql = "select * from STKLIST where EXCHID = '0' and REGID in( '0000301528','A117203000','A117392000') " \
                      "and STKID in ('020056','130291') and DESKID = '00W40' "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0' " \
                         "and  stkid in ('020056','130291') and briefid in('005_002_001'," \
                         "'005_001_001')".format(year,begintime,endtime)
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklistcurrent_database = base.stklist_sort(oracle.dict_data(stklistcurrent_sql))

        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist2021'))
        stklistcurrent_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        # 忽略字段
        account_ignore = ()
        stklist_ignore = ('OCCURTIME',)
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        # exchangerights_ignore = ()
        # 对比
        # account_result = base.compare_dict(account_database, account_excel, 'account')
        stklistcurrent_result = base.compare_dict(stklistcurrent_database, stklistcurrent_excel, 'stklist')

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist2022',*stklist_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result =  stklistcurrent_result+stklist_result + tradinglog_result
        if not final_result:
            logger().info('沪A/合并申报 对比数据无异常')
            assert True
        else:
            logger().error('沪A/合并申报 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
