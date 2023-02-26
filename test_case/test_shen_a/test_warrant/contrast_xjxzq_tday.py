import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深A\权证行权\现金选择权\权证登记
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['XJXZQ']['Tday']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深A\权证行权\现金选择权\权证登记
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\权证行权\现金选择权\权证登记 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql   只查034088持仓，034089持仓权证行权会变化
        stklist_sql = "select * from stklist where exchid='1' and  stkid='034088' "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1'  " \
                         "and stkid in ('034089','034088','034098') and briefid='005_003_008'".format(year, begintime, endtime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        # 对比

        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        # 断言
        final_result =  stklist_result
        if not final_result:
            logger().info('深A\权证行权\现金选择权\权证登记 对比数据无异常')
            assert True
        else:
            logger().error('深A\权证行权\现金选择权\权证登记 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
