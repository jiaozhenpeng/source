
import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation

class ContrastTgzf(unittest.TestCase):
    '''
    深银行\互联互通数据 9位代码\TGZF
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())
    def test_tgzf(self):
        '''
        市场B\互联互通数据 9位代码\TGZF
        :return:
        '''
        logger().info('-----------------------')
        logger().info('开始对比  深银行\互联互通数据 9位代码\TGZF  场景')
        test_yaml = ContrastTgzf().yaml['Tgzf']
        excel_path = test_yaml['excelPath']
        stklist_sql = test_yaml['stklist_sql']
        tradinglog_sql = test_yaml['tradinglog_sql']
        exchangerights_sql = test_yaml['exchangerights_sql']
        stklistextend_sql = test_yaml['stklistextend_sql']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        # 对比表时可以忽略的字段
        account_ignore = []
        stklist_ignore = []
        # 获取数据库表数据
        stklist_database = oracle.dict_data(stklist_sql)
        tradinglog_database = oracle.dict_data(tradinglog_sql)
        exchangerights_database = oracle.dict_data(exchangerights_sql)
        stklistextend_database = oracle.dict_data(stklistextend_sql)
        # 获取Excel预期结果
        stklist_excel = excel.read_excel('stklist')
        tradinglog_excel = excel.read_excel('tradinglog')
        exchangerights_excel = excel.read_excel('exchangerights')
        stklistextend_excel = oracle.dict_data('stklistextend')
        # 排序
        stklist_database.sort(key=lambda x: (x['ACCTID'], x['CUSTID']))
        stklist_excel.sort(key=lambda x: (x['ACCTID'], x['CUSTID']))
        tradinglog_database.sort(key=lambda x: x['SERIALNUM'])
        tradinglog_excel.sort(key=lambda x: x['SERIALNUM'])
        exchangerights_database.sort(key=lambda x: x['SERIALNUM'])
        exchangerights_excel.sort(key=lambda x: x['SERIALNUM'])
        stklistextend_database.sort(key=lambda x: (x['SHAREATTR'], x['LISTEDSTATUS']))
        stklistextend_excel.sort(key=lambda x: (x['SHAREATTR'], x['LISTEDSTATUS']))
        # 对比数据库与Excel的结果,后面可根据需求补充不需要对比的字段
        stklistextend_result = BaseAction().compare_dict(stklistextend_database, stklistextend_excel,'stklistextend')
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel,'stklist')
        exchangerights_result = BaseAction().compare_dict(exchangerights_database, exchangerights_excel,'exchangerights')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel,'tradinglog')

        if not stklist_result and not tradinglog_result and not exchangerights_result and not stklistextend_result :
            # 对比结果都为空时证明无异常数据
            logger().info('深银行\互联互通数据 9位代码\TGZF  对比无异常')
            assert True
        else:
            logger().error('深银行\互联互通数据 9位代码\TGZF，异常')
            assert False ,stklistextend_result + stklist_result + exchangerights_result + tradinglog_result

if __name__ == '__main__':
    unittest.main()
