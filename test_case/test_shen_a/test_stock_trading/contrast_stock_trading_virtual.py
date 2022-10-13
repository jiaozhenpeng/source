import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastStockTrading(unittest.TestCase):
    """
    深A\股票买入虚拟股东
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['StockTradeVirtual']

    def test_Stock_Trading(self):
        """
        深A\股票买入虚拟股东
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\股票买入虚拟股东 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        account_sql = "select * from  account where acctid ='000011728201' and currencyid='00'"
        stklist_sql = "select * from stklist where exchid='1' and stkid='000001' and regid='0117282001' "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         "  regid='0117282001' and stkid in ('000001') and briefid in('005_001_001')".format(year,begintime,endtime)
        # 数据库数据
        account_database = base.account_sort(oracle.dict_data(account_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        account_excel = base.account_sort(excel.read_excel('account'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        # 忽略字段
        openorder_ignore = ()
        account_ignore = ()
        stklist_ignore = ()
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        # 对比
        account_result = base.compare_dict(account_database, account_excel, 'account')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result =  account_result +stklist_result + tradinglog_result
        if not final_result:
            logger().info('深A\股票买入虚拟股东 对比数据无异常')
            assert True
        else:
            logger().error('深A\股票买入虚拟股东 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
