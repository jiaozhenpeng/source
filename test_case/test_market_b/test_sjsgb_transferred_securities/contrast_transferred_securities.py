import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation

class ContrastTransferredSecurities(unittest.TestCase):
    '''
    对比数据：市场B\sjsgb转入证券信息
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().market_b())
    def test_transferred_securities(self):
        '''
        对比数据：市场B\sjsgb转入证券信息
        :return:
        '''
        logger().info('--------------------')
        logger().info('对比市场B\sjsgb转入证券信息数据')
        test_yaml = ContrastTransferredSecurities().yaml['TransferredSecurities']
        stkinfo_sql = test_yaml['stkinfo_sql']
        stkcheckin_sql = test_yaml['stkcheckin_sql']
        excel_path = test_yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        # 对比表时可以忽略的字段
        stkinfo_ignore = ('INPUTTIME',)
        stkcheckin_ignore = ('OCCURTIME','BONUSRECEIVEDDATE')
        # 获取数据库表数据
        stkinfo_database = oracle.dict_data(stkinfo_sql)
        stkcheckin_database = oracle.dict_data(stkcheckin_sql)
        # 获取Excel预期结果
        stkinfo_excel = excel.read_excel('stkinfo')
        stkcheckin_excel = excel.read_excel('stkcheckin')
        # 排序
        stkinfo_database.sort(key=lambda x: x['STKID'])
        stkcheckin_database.sort(key=lambda x: x['STKID'])
        stkinfo_excel.sort(key=lambda x: x['STKID'])
        stkcheckin_excel.sort(key=lambda x: x['STKID'])
        # 对比数据库与Excel的结果，后面可根据需求补充不需要对比的字段
        stkinfo_result = BaseAction().compare_dict(stkinfo_database, stkinfo_excel,'stkinfo')
        stkcheckin_result = BaseAction().compare_dict(stkcheckin_database, stkcheckin_excel,'stkcheckin')
        if not stkcheckin_result and not stkinfo_result:
            logger().info('市场B\sjsgb转入证券信息数据对比无误')
            assert True
        else:
            logger().error('市场B\sjsgb转入证券信息数据对比异常')
            assert False,stkcheckin_result+stkinfo_result
if __name__ == '__main__':
    unittest.main()

