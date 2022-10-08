import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEquityDistribution(unittest.TestCase):
    """
    沪A\上海配股配债\T日权益发放
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['MatchThighDebt']['EquityDistribution']

    def test_equity_distribution(self):
        """
        沪A\上海配股配债\T日权益发放
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\上海配股配债\T日权益发放 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        regrights_sql = "select * from regrights where EXCHID='0' and STKID in ('700489','760099') and REGID in" \
                        " ('A117605000','A117605001') and DESKID ='00W40'"
        exchangerights_sql = "select * FROM exchangerights  where exchid='0' and stkid in ('700489','760099') and" \
                             " DESKID ='00W40' and REGID in ('A117605000','A117605001')"
        stklist_sql = "select * from STKLIST where EXCHID = '0' and REGID in('A117605000','A117605001') and STKID" \
                      " in ('A117605000','A117605001') and DESKID = '00W40'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and REGID in('A117605000','A117605001') and  stkid in ('700489','760099') and DESKID" \
                         " ='00W40'".format(year, begintime, endtime)
        # 数据库数据
        regrights_database = base.regrights_sort(oracle.dict_data(regrights_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        regrights_excel = base.regrights_sort(excel.read_excel('regrights'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 忽略字段
        regrights_ignore = ()
        exchangerights_ignore = ()
        stklist_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        # 对比
        regrights_result = base.compare_dict(regrights_database, regrights_excel, 'regrights')
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result = regrights_result + exchangerights_result + stklist_result + tradinglog_result
        if not final_result:
            logger().info('沪A\上海配股配债\T日权益发放 对比数据无异常')
            assert True
        else:
            logger().error('沪A\上海配股配债\T日权益发放 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()