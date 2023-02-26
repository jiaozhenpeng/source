import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastBondDistribution(unittest.TestCase):
    """
    深A\ETF申赎\沪深北ETF\T日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['HSBSH']['Tday']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_bond_distribution(self):
        """
        深A\ETF申赎\沪深北ETF\T日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\ETF申赎\沪深北ETF\T日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql

        stklist_sql = "select * from STKLIST where  EXCHID = '1' and REGID in ('0999900007'," \
                      "'0666600007') and stkid in('002797','300741','159968' ) and DESKID = '077011'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and" \
                         "  stkid in('002797','300741','159968','159900','000063') and briefid in( '005_001_002','005_001_003'," \
                         "'005_002_003','005_002_002','005_002_025')  and contractnum in('00020002','00020046')".format(year, begintime, endtime)
        unprocessedreckoningresult_sql = "select * from unprocessedreckoningresult where knocktime={} and briefid in(" \
                                         " '005_001_019','005_001_002','005_002_019','005_002_002') and stkid in('159968')" \
                                         " and exchid='1' and contractnum in('00020002','00020046')".format(begintime,)
        unprocessedreckoningresulthis_sql = "select * from unprocessedreckoningresulthis where knocktime={} and briefid in(" \
                                         " '005_001_019','005_001_002','005_002_019','005_002_002') and stkid in('159968')" \
                                         " and exchid='1' and contractnum in('00020002','00020046')".format(begintime,)
        etfcashrefillwait_sql = "select * from etfcashrefillwait where exchid='1' and fundcode='159968' " \
                                "and occurtime = {}".format(begintime,)
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(oracle.dict_data(unprocessedreckoningresult_sql))
        unprocessedreckoningresulthis_database = base.unprocessedreckoningresulthis_sort(oracle.dict_data(unprocessedreckoningresulthis_sql))
        etfcashrefillwait_database = base.etfcashrefillwait_sort(oracle.dict_data(etfcashrefillwait_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2023'))
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(excel.read_excel('unprocessedreckoningresult'))
        unprocessedreckoningresulthis_excel = base.unprocessedreckoningresulthis_sort(excel.read_excel('unprocessedreckoningresulthis'))
        etfcashrefillwait_excel = base.etfcashrefillwait_sort(excel.read_excel('etfcashrefillwait'))
        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        unprocessedreckoningresult_ignore = self.ignore['unprocessedreckoningresult']
        unprocessedreckoningresulthis_ignore = self.ignore['unprocessedreckoningresulthis']
        etfcashrefillwait_ignore = self.ignore['etfcashrefillwait']

        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,unprocessedreckoningresult_excel,
                                                              'unprocessedreckoningresult',*unprocessedreckoningresult_ignore)
        unprocessedreckoningresulthis_result = base.compare_dict(unprocessedreckoningresulthis_database,unprocessedreckoningresulthis_excel,
                                                              'unprocessedreckoningresulthis',*unprocessedreckoningresulthis_ignore)
        etfcashrefillwait_result = base.compare_dict(etfcashrefillwait_database,etfcashrefillwait_excel,
                                                     'etfcashrefillwait',*etfcashrefillwait_ignore)
        # 断言
        final_result =  stklist_result +  tradinglog_result + unprocessedreckoningresult_result + unprocessedreckoningresulthis_result
        if not final_result:
            logger().info('深A\ETF申赎\沪深北ETF\T日 对比数据无异常')
            assert True
        else:
            logger().error('深A\ETF申赎\沪深北ETF\T日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()

