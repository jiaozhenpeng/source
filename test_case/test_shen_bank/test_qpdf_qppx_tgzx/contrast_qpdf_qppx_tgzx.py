import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastQpdfQppxTgzx(unittest.TestCase):
    '''
    深银行\QPDF QPPX TGZX

    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())  # 获取yaml文件
    def test_test_qpdf_qppx_tgzx(self):
        '''
        深银行\QPDF QPPX TGZX
        :return:
        '''
        logger().info('-----------------------')
        logger().info('开始对比 深银行\QPDF QPPX TGZX 场景')
        test_yaml = ContrastQpdfQppxTgzx().yaml['qpdf_qppx_tgzx']
        excel_path = test_yaml['excelPath']
        account_sql = test_yaml['account_sql']
        stklist_sql = test_yaml['stklist_sql']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        # 对比表时可以忽略的字段
        account_ignore = []
        stklist_ignore = []
        # 获取数据库表数据
        account_database = oracle.dict_data(account_sql)
        stklist_database = oracle.dict_data(stklist_sql)
        # 获取Excel预期结果
        account_excel = excel.read_excel('account')
        stklist_excel = excel.read_excel('stklist')
        # 排序
        account_database.sort(key=lambda x : x ['ACCTID'])
        stklist_database.sort(key=lambda x : x ['ACCTID'])
        account_excel.sort(key=lambda x : x ['ACCTID'])
        stklist_excel.sort(key=lambda x : x ['ACCTID'])
        # 对比数据库与Excel的结果,后面可根据需求补充不需要对比的字段
        account_result = BaseAction().compare_dict(account_database,account_excel,'account')
        stklist_result = BaseAction().compare_dict(stklist_database,stklist_excel,'stklist')

        if not account_result and not stklist_result : # 对比结果都为空时证明无异常数据
            logger().error('深银行\QPDF QPPX TGZX 对比无异常')
            assert True
        else:
            logger().info('深银行\QPDF QPPX TGZX 对比异常，异常数据：{}，{}'.format(account_result,stklist_result))
            assert False ,account_result + stklist_result
if __name__ == '__main__':
    unittest.main()
