import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralLiquidation(unittest.TestCase):
    """
    沪权\特殊资金处理
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['specacct']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_general_liquid(self):
        """
        沪权\特殊资金处理
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\特殊资金处理 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[0:4]
        # 查询SQL

        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and " \
                               "exchid='X' and briefid in('208_002_042','208_002_041')".format(year, begintime, endtime)

        # 获取数据库数据
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # excel 数据
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))

        # 忽略字段
        futuretradinglog_ignore = self.ignore['futuretradinglog']


        # 对比结果
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog',*futuretradinglog_ignore)

        # 断言
        final_result = futuretradinglog_result

        if not final_result :
            logger().info('沪权\特殊资金处理 对比数据无异常')
            assert True
        else:
            logger().error('沪权\特殊资金处理 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
