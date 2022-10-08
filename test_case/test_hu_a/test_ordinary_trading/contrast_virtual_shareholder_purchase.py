import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastVirtualShareholderPurchase(unittest.TestCase):
    """
    沪A\普通买卖\股票买入虚拟股东
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['OrdinaryTrading']['VirtualShareholderPurchase']

    def test_virtual_shareholder_purchase(self):
        """
        沪A\普通买卖\股票买入虚拟股东
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\普通买卖\股票买入虚拟股东 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST{} where EXCHID = '0' and REGID = 'A117292001' and STKID = '600000' " \
                      "and DESKID = '00W40' and OCCURTIME = {}".format(year,begintime)
        account_sql = "select * from ACCOUNT{} where ACCTID = '000011729201' and CURRENCYID='00'  and " \
                      "OCCURTIME = {}".format(year,begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0' " \
                         "and  STKID = '600000' and briefid ='005_001_001' and REGID = 'A117292001'".format(year,begintime,endtime)
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        account_database = base.account_sort(oracle.dict_data(account_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist2021'))
        account_excel = base.account_sort(excel.read_excel('account2021'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 忽略字段
        stklist_ignore = ()
        account_ignore = ()
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        account_result = base.compare_dict(account_database, account_excel, 'account')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result = stklist_result + account_result + tradinglog_result
        if not final_result:
            logger().info('沪A\普通买卖\股票买入虚拟股东 对比数据无异常')
            assert True
        else:
            logger().error('沪A\普通买卖\股票买入虚拟股东 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()