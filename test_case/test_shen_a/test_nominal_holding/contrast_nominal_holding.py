import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastNominalHolding(unittest.TestCase):
    """
    深A\名义持有明细股份管理
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['NominalHolding']

    def test_NominalHolding(self):
        """
        深A\名义持有明细股份管理
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\名义持有明细股份管理 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        NominalholdingHis_sql = "select * from NominalholdingHis  where knocktime>={} and knocktime<={} ".format(begintime,endtime)
        # 数据库数据
        NominalholdingHis_database = base.nominalholdingHis_sort(oracle.dict_data(NominalholdingHis_sql))
        # Excel数据
        NominalholdingHis_excel = base.nominalholdingHis_sort(excel.read_excel('NominalholdingHis'))
        # 忽略字段
        NominalholdingHis_ignore =('KNOCKTIME',)
        # 对比
        NominalholdingHis_result = base.compare_dict(NominalholdingHis_database,NominalholdingHis_excel,
                                                      'NominalholdingHis',*NominalholdingHis_ignore)
        # 断言
        final_result = NominalholdingHis_result
        if not final_result:
            logger().info('深A\名义持有明细股份管理 对比数据无异常')
            assert True
        else:
            logger().error('深A\名义持有明细股份管理 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
