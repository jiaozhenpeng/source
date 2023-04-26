import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深A\权证行权\股权激励\权证登记
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['GQJL']['Tday']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深A\权证行权\股权激励\权证登记
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\权证行权\股权激励\权证登记 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql   只查034088持仓，034089持仓权证行权会变化
        stklist_sql = "select * from stklist where exchid='1' and  stkid in('038029','038033','038036')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1'  " \
                         "and stkid in ('038029','038033','038036') and briefid in('005_003_081','005_003_083'," \
                         "'005_004_082')".format(year, begintime, endtime)
        stklistextendhis = "select * from   stklistextend{} where occurtime={} and exchid='1' and stkid " \
                           "in('038029','038033','038036')".format(year, begintime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklistextendhid_database = base.stklistextend_sort(oracle.dict_data(stklistextendhis))

        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklistextendhis_excel = base.stklistextend_sort(excel.read_excel('stklistextend2023'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        stklistextendhis_ignore = self.ignore['stklistextendhis']
        # 对比

        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextendhis_result = base.compare_dict(stklist_database,stklist_excel,'stklist2023',*stklistextendhis_ignore)
        # 断言
        final_result =  stklist_result + tradinglog_result + stklistextendhis_result
        if not final_result:
            logger().info('深A\权证行权\股权激励\权证登记 对比数据无异常')
            assert True
        else:
            logger().error('深A\权证行权\股权激励\权证登记 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
