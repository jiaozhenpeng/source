import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    股转\DVP改革\可售交收冻结（T日）
    """
    yaml = BaseAction().read_yaml(path=PathConfig().share_reconciliation())['DVP']['Tday']

    def test_restricted_shares(self):
        """
        股转\DVP改革\可售交收冻结（T日）
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转\DVP改革\可售交收冻结（T日） 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklistextend_sql = " select * from  stklistextend where exchid='6' and offerregid in('GZ11721600','0899065379')" \
                            " and stkid in('871238','830928','810002','430529')"
        stklist_sql = "select * from  stklist where exchid='6' and offerregid in('GZ11721600','0899065379') " \
                      "and stkid in('871238','830928','810002','430529')"
        # 获取数据库数据并排序

        stklistextend_database = BaseAction().stklistextend_sort(oracle.dict_data(stklistextend_sql))
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        # 获取excel数据并排序
        stklistextend_excel = BaseAction().stklistextend_sort(excel.read_excel('stklistextend'))
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        # 可以忽略的字段
        stklistextend_ignore = ()
        stklist_ignore = ()
        # 对比数据

        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextend_result = BaseAction().compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        final_result = stklist_result + stklistextend_result

        # 断言
        if not final_result:
            logger().info('沪A\DVP改革\可售交收冻结（T日） 对比数据无异常')
            assert True
        else:
            logger().error('沪A\DVP改革\可售交收冻结（T日） 对比数据异常')
            assert False, final_result

    if __name__ == '__main__':
        unittest.main()