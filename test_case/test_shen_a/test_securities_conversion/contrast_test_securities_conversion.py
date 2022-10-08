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

    def test_securities_conversion(self):
        '''
        测试 证券转换
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 深A/证券转换  数据')
        excel_path = self.yaml['excel']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        base = BaseAction()
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '1' and REGID in( '0117212000','0117212001','0117252000'," \
                      "'0117252001') and STKID in ('184721','184720') and DESKID = '077011'"
        # 查询数据库数据并排序
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        # 查询excel数据
        stklist_excel =base.stklist_sort(excel.read_excel('stklist'))
        # 忽略字段
        stklist_ignore =()
        # 对比结果
        stklist_result =base.compare_dict(stklist_database,stklist_excel,'stklist')
        # 断言
        if not stklist_result:
            logger().info('深A/证券转换 数据对比无异常')
            assert True
        else:
            logger().error('深A/证券转换 数据对比异常:{}'.format(stklist_result))
            assert False, stklist_result

if __name__ == '__main__':
    unittest.main()