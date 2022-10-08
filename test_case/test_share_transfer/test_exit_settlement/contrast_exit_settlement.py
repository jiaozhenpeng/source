import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastExitSettlement(unittest.TestCase):
    """
    对比 股转\退出结算系统
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['ExitSettlement']

    def test_exit_settlement(self):
        """
        对比 股转\退出结算系统
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 股转\退出结算系统 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        base = BaseAction()
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID = 'GZ11721600' and STKID = '839110' and DESKID = 'ANQ001'"
        stklistextend_sql = "select * FROM stklistextend a where a.exchid='6' and a.stkid = '839110' and DESKID ='ANQ001' and REGID = 'GZ11721600'"
        # 查询数据库
        print(oracle.dict_data(stklist_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        print(stklist_database)
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        # 查询excel
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        # 忽略字段
        stklist_ignore = ()
        stklistextend_ignore = ()
        # 对比结果
        stklist_result = base.compare_dict(stklist_database,stklist_excel,'stklist')
        stklistextend_result = base.compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')
        # 断言
        final_result = stklist_result + stklistextend_result
        if not final_result:
            logger().info('股转\退出结算系统 数据对比无异常')
            assert True
        else:
            logger().error('股转\退出结算系统 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()

