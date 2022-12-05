import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深银行\普通交易\卖出
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())['trade']['sell']

    def test_etf_split(self):
        """
        深银行\普通交易\卖出
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深银行\普通交易\卖出 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where exchid='B' and stkid in('2102001QF','092103107') "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= 'B'  " \
                         "and stkid in ('2102001QF','092103107') ".format(year,begintime,endtime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))

        # 忽略字段
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
            'POSTAMT')
        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result =  stklist_result+ tradinglog_result
        if not final_result:
            logger().info('深银行\普通交易\卖出 对比数据无异常')
            assert True
        else:
            logger().error('深银行\普通交易\卖出 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
