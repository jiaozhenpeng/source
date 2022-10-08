import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation

class ContrastTzgf(unittest.TestCase):
    '''
    场景 深银行\互联互通数据 9位代码\TZGF 对比数据
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())
    def test_tzgf(self):
        '''
        对比数据：市场B\互联互通数据 9位代码\TZGF
        :return:
        '''
        logger().info('--------------------')
        logger().info('对比 深银行\互联互通数据 9位代码\TZGF 数据')
        test_yaml = ContrastTzgf().yaml['tzgf']
        # 需要对比的sql
        stklistextend_sql = test_yaml['stklistextend_sql']
        stklist_sql = test_yaml['stklist_sql']
        exchangerights_sql = test_yaml['exchangerights_sql']
        tradinglog_sql = test_yaml['tradinglog_sql']
        stkinfo_sql = test_yaml['stkinfo_sql']
        VirtualRegistrationRights_sql = test_yaml['VirtualRegistrationRights_sql']
        excel_path = test_yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        # 对比表时可以忽略的字段
        stkinfo_ignore = ()
        stkcheckin_ignore = ()
        # 获取数据库表数据
        stklistextend_database = oracle.dict_data(stklistextend_sql)
        stklist_database = oracle.dict_data(stklist_sql)
        exchangerights_database = oracle.dict_data(exchangerights_sql)
        tradinglog_database = oracle.dict_data(tradinglog_sql)
        stkinfo_database = oracle.dict_data(stkinfo_sql)
        VirtualRegistrationRights_database = oracle.dict_data(VirtualRegistrationRights_sql)
        # 获取Excel预期结果
        stklistextend_excel = excel.read_excel('stklistextend')
        stklist_excel = excel.read_excel('stklist')
        exchangerights_excel = excel.read_excel('exchangerights')
        tradinglog_excel = excel.read_excel('tradinglog')
        stkinfo_excel = excel.read_excel('stkinfo')
        VirtualRegistrationRights_excel = excel.read_excel('VirtualRegistrationRights')
        # 排序
        stklistextend_database.sort(key=lambda x: (x['SHAREATTR'],x['LISTEDSTATUS']))
        stklistextend_excel.sort(key=lambda x: (x['SHAREATTR'],x['LISTEDSTATUS']))
        stklist_database.sort(key=lambda x: (x['UNSALEABLEQTY'],x['PREVIOUSCOST']))
        stklist_excel.sort(key=lambda x: (x['UNSALEABLEQTY'],x['PREVIOUSCOST']))
        exchangerights_database.sort(key=lambda x: (x['SERIALNUM'],x['RECKONINGSERIALNUM']))
        exchangerights_excel.sort(key=lambda x: (x['SERIALNUM'],x['RECKONINGSERIALNUM']))
        tradinglog_database.sort(key=lambda x: x['SERIALNUM'])
        tradinglog_excel.sort(key=lambda x: x['SERIALNUM'])
        stkinfo_database.sort(key=lambda x: x['MINSELLSTKQTY'])
        stkinfo_excel.sort(key=lambda x: x['MINSELLSTKQTY'])
        VirtualRegistrationRights_database.sort(key=lambda x: x['SERIALNUM'])
        VirtualRegistrationRights_excel.sort(key=lambda x: x['SERIALNUM'])
        # 对比数据库与Excel的结果，后面可根据需求补充不需要对比的字段
        stklistextend_result = BaseAction().compare_dict(stklistextend_database, stklistextend_excel,'stklistextend')
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel,'stklist')
        exchangerights_result = BaseAction().compare_dict(exchangerights_database, exchangerights_excel,'exchangerights')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel,'tradinglog')
        stkinfo_result = BaseAction().compare_dict(stkinfo_database, stkinfo_excel,'stkinfo')
        VirtualRegistrationRights_result = BaseAction().compare_dict(VirtualRegistrationRights_database, VirtualRegistrationRights_excel)
        if not stklistextend_result and not stklist_result and exchangerights_result and not tradinglog_result and not stkinfo_result\
                and not VirtualRegistrationRights_result:
            logger().info('深银行\互联互通数据 9位代码\TZGF 数据对比无误')
            assert True
        else:
            logger().error('深银行\互联互通数据 9位代码\TZGF 数据对比异常')
            assert False, stklistextend_result + stklist_result and exchangerights_result + tradinglog_result + stkinfo_result\
                + VirtualRegistrationRights_result

if __name__ == '__main__':
    unittest.main()

