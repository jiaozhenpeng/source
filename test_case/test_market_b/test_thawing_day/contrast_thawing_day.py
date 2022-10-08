import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastThawingDay(unittest.TestCase):
    '''
    市场B\冻结变更和冻结结息\解冻日
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().market_b())

    def test_thawing_day(self):
        '''
        市场B\冻结变更和冻结结息\兑付冻结解冻
        :return:
        '''
        logger().info('--------------------')
        logger().info('对比  市场B\冻结变更和冻结结息\解冻日')
        test_yaml = ContrastThawingDay().yaml['ThawingDay']
        # 需要对比的sql
        account_sql = test_yaml['account_sql']
        stklist_sql = test_yaml['stklist_sql']
        tradinglog_sql = test_yaml['tradinglog_sql']
        exchangerights_sql = test_yaml['exchangerights_sql']
        excel_path = test_yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        # 对比表时可以忽略的字段
        stkinfo_ignore = ()
        stkcheckin_ignore = ()
        # 获取数据库表数据
        account_database = oracle.dict_data(account_sql)
        stklist_database = oracle.dict_data(stklist_sql)
        tradinglog_database = oracle.dict_data(tradinglog_sql)
        exchangerights_database = oracle.dict_data(exchangerights_sql)
        # 获取Excel预期结果
        account_excel = excel.read_excel('account')
        stklist_excel = excel.read_excel('stklist')
        tradinglog_excel = excel.read_excel('tradinglog')
        exchangerights_excel = excel.read_excel('exchangerights')
        # 排序
        account_database.sort(key=lambda x: x['ACCTID'])
        account_excel.sort(key=lambda x: x['ACCTID'])
        stklist_database.sort(key=lambda x: (x['ACCTID'], x['CUSTID']))
        stklist_excel.sort(key=lambda x: (x['ACCTID'], x['CUSTID']))
        tradinglog_database.sort(key=lambda x: x['SERIALNUM'])
        tradinglog_excel.sort(key=lambda x: x['SERIALNUM'])
        exchangerights_database = BaseAction().exchangerights_sort(exchangerights_database)
        exchangerights_excel = BaseAction().exchangerights_sort(exchangerights_excel)
        # 对比数据
        account_result = BaseAction().compare_dict(account_database, account_excel,'account')
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel,'stklist')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel,'tradinglog')
        exchangerights_result = BaseAction().compare_dict(exchangerights_database, exchangerights_excel,'exchangerights')
        if not account_result and not stklist_result and not tradinglog_result and not exchangerights_result:
            logger().info('市场B\冻结变更和冻结结息\解冻日 数据对比无误')
            assert True
        else:
            logger().error('市场B\冻结变更和冻结结息\解冻日 数据对比异常')
            assert False, account_result + stklist_result + tradinglog_result + exchangerights_result

if __name__ == '__main__':
    unittest.main()
