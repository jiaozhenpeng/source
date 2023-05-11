import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深A\债券质押式回购\现金担保品
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['bondrepo']['xjdbp']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深A\债券质押式回购\现金担保品
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\债券质押式回购\现金担保品 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        stklistextend_sql = "select * from STKLISTEXTEND where exchid='1' and stkid in('131990') "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1'  " \
                         "and briefid in ('005_005_086','005_005_087') ".format(year, begintime, endtime)

        # 数据库数据
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # Excel数据
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        # 对比

        stklist_result = base.compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result =  stklist_result
        if not final_result:
            logger().info('深A\债券质押式回购\现金担保品 对比数据无异常')
            assert True
        else:
            logger().error('深A\债券质押式回购\现金担保品 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
