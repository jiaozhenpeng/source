import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深A\高管可划拨额度
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['gaoguan']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深A\高管可划拨额度
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\高管可划拨额度 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklistextend_sql = "select * from stklistextend where exchid ='1' and  stkid in('000402','000748') and regid='0117252000' "
        stklist_sql = "select * from stklist where exchid ='1' and  stkid in('000402','000748') and regid='0117252000'"

        # 数据库数据
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        # Excel数据
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))

        # 忽略字段
        # stklistextend_ignore = self.ignore['stklistextend']
        # 对比

        stklistextend_result = base.compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        stklist_result = base.compare_dict(stklist_database,stklist_excel,'stklist')
        # 断言
        final_result =  stklistextend_result
        if not final_result:
            logger().info('深A\高管可划拨额度 对比数据无异常')
            assert True
        else:
            logger().error('深A\高管可划拨额度 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
