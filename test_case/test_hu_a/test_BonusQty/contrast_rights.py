import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\红股\权益发送日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['BonusQty']['rights']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪A\红股\权益发送日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\红股\权益发送日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from stklist where exchid='0' and stkid in('603393','603392') "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid in ('603393','603392')  ".format(year, begintime, endtime)
        stkcheckin_sql = "select * from   stkcheckin where exchid='0' and stkid in ('603393','603392')"

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stkcheckin_database = base.stkcheckin_sort(oracle.dict_data(stkcheckin_sql))

        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stkcheckin_excel = base.stkcheckin_sort(excel.read_excel('stkcheckin'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        stkcheckin_ignore = self.ignore['stkcheckin']
        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stkcheckin_result = base.compare_dict(stkcheckin_database,stkcheckin_excel,'stkcheckin',*stkcheckin_ignore)
        # 断言
        final_result =  stklist_result + tradinglog_result + stkcheckin_result
        if not final_result:
            logger().info('沪A\红股\权益发送日 对比数据无异常')
            assert True
        else:
            logger().error('沪A\红股\权益发送日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
