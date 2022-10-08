import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastBusiness(unittest.TestCase):
    """
    深港\\买卖
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_gang())['Business']

    def test_shen_business(self):
        logger().info('-------------------------------')
        logger().info('开始执行：深港\\买卖 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '4' and REGID in( '0117222000','0117222001') and STKID " \
                      "in ('00476','23131','01217') and DESKID = '077011'"
        unprocessedreckoningresult_sql = "select * from unprocessedreckoningresult where STKID in " \
                                         "('00476','23131','01217') and DESKID = '077011' and EXCHID = '4' and " \
                                         "REGID in( '0117222000','0117222001')"
        # 需要忽略的字段
        stklist_ignore = ()
        unprocessedreckoningresult_ignore = ()
        # 获取数据库数据并排序
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        unprocessedreckoningresult_database = BaseAction().unprocessedreckoningresult_sort(
            oracle.dict_data(unprocessedreckoningresult_sql))
        # 获取excel数据并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        unprocessedreckoningresult_excel = BaseAction().unprocessedreckoningresult_sort(
            excel.read_excel('unprocessedreckoningresult'))
        # 对比数据
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        unprocessedreckoningresult_result = BaseAction().compare_dict(unprocessedreckoningresult_database,
                                                                      unprocessedreckoningresult_excel,
                                                                      'unprocessedreckoningresult')
        if not stklist_result and not unprocessedreckoningresult_result:
            logger().info('深港\\买卖T日清算 对比数据无异常')
            assert True
        else:
            logger().error('深港\\买卖T日清算 对比数据异常')
            assert False, stklist_result + unprocessedreckoningresult_result


if __name__ == '__main__':
    unittest.main()
