import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastDateOfPayment(unittest.TestCase):
    """
     深A\红股红利\兑付\兑付当日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['BonusShares']['DateOfPayment']

    def test_date_of_payment(self):
        """
         深A\红股红利\兑付\兑付当日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行： 深A\红股红利\兑付\兑付当日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST{} where EXCHID = '1' and REGID in( '0117212000','0117212001','0117252000'," \
                      "'0117252001') and STKID = '118311' and DESKID = '077011' and OCCURTIME = {}".format(year,begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and" \
                         "  stkid = '118311' and briefid in('005_005_002','005_005_026','005_004_002'," \
                         "'005_005_063')".format(year,begintime,endtime)
        stkcheckin_sql = "select * from stkcheckin where EXCHID ='1' and STKID ='118311' and OCCURTIME ={} ".format(begintime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stkcheckin_database = base.stkcheckin_sort(oracle.dict_data(stkcheckin_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist2022'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2022'))
        stkcheckin_excel = base.stkcheckin_sort(excel.read_excel('stkcheckin'))
        # 忽略字段
        stklist_ignore = ('OCCURTIME',)
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        stkcheckin_ignore =('OCCURTIME','KEEPTODATE','BONUSRECEIVEDDATE')
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist',*stklist_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stkcheckin_result = base.compare_dict(stkcheckin_database,stkcheckin_excel,'stkcheckin',*stkcheckin_ignore)
        # 断言
        final_result = stklist_result + tradinglog_result + stkcheckin_result
        if not final_result:
            logger().info(' 深A\红股红利\兑付\兑付当日 对比数据无异常')
            assert True
        else:
            logger().error(' 深A\红股红利\兑付\兑付当日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
