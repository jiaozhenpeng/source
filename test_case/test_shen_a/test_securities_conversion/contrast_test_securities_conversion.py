import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastSecuritiesConversion(unittest.TestCase):
    """
    测试 证券转换
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['SecuritiesConversion']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_securities_conversion(self):
        '''
        测试 证券转换
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 深A/证券转换  数据')
        excel_path = self.yaml['excel']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '1' and REGID in( '0117212000','0117212001','0117252000'," \
                      "'0117252001') and STKID in ('184721','184720') and deskid = '077011'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and" \
                         " stkid in('184721','184720') ".format(year, begintime, endtime)
        stklistextend_sql = "select * from stklistextend where EXCHID = '1' and REGID in( '0117212000','0117212001','0117252000'," \
                      "'0117252001') and STKID in ('184721','184720') and deskid = '077011'"
        # 查询数据库数据并排序
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort4(oracle.dict_data(tradinglog_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        # 查询excel数据
        stklist_excel =base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort4(excel.read_excel('tradinglog'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        # 对比结果
        stklist_result =base.compare_dict(stklist_database,stklist_excel,'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
        stklistextend_result = base.compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')
        final_result = stklist_result + tradinglog_result + stklistextend_result
        # 断言
        if not final_result:
            logger().info('深A/证券转换 数据对比无异常')
            assert True
        else:
            logger().error('深A/证券转换 数据对比异常:{}'.format(stklist_result))
            assert False, stklist_result

if __name__ == '__main__':
    unittest.main()