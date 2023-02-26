import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深A\资金前端控制
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['zjqdkz']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深A\资金前端控制
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\资金前端控制 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql   只查034088持仓，034089持仓权证行权会变化
        fundquota_sql = "select * from fundquota where exchid in('1','3') and  occurtime={} ".format(begintime,)

        # 数据库数据
        fundquota_database = base.fundquota_sort(oracle.dict_data(fundquota_sql))

        # Excel数据
        fundquota_excel = base.fundquota_sort(excel.read_excel('fundquota'))

        # 忽略字段
        fundquota_ignore = self.ignore['fundquota']
        # 对比

        fundquota_result = base.compare_dict(fundquota_database, fundquota_excel, 'fundquota',*fundquota_ignore)
        # 断言
        final_result =  fundquota_result
        if not final_result:
            logger().info('深A\资金前端控制 对比数据无异常')
            assert True
        else:
            logger().error('深A\资金前端控制 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
