import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪银行\兑息\子股东
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_bank())['qpdx']['zigudong']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪银行\兑息\子股东
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪银行\兑息\子股东 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from stklist where exchid='C' and  stkid='092100012' "
        stklisthis_sql = " select * from    stklist{} where occurtime={} and   exchid= 'C'  and " \
                         "stkid in ('092100012')".format(year, begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= 'C'  " \
                         "and stkid in ('092100012') ".format(year, begintime, endtime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklisthis_database = base.stklist_sort(oracle.dict_data(stklisthis_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklisthis_excel = base.stklist_sort(excel.read_excel('stklist2022'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        stklisthis_ignore = self.ignore['stklisthis']
        # 对比

        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklisthis_result = base.compare_dict(stklisthis_database, stklisthis_excel, 'stklist2022', *stklisthis_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')

        # 断言
        final_result = tradinglog_result + stklisthis_result + stklist_result
        if not final_result:
            logger().info('沪银行\兑息\子股东 对比数据无异常')
            assert True
        else:
            logger().error('沪银行\兑息\子股东 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
