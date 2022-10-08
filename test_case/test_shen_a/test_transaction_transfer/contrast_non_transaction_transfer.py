import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastNonTransactionTransfer(unittest.TestCase):
    """
    对比 深A\非交易转让
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['NonTransactionTransfer']

    def test_non_transaction_transfer(self):
        """
        深A\非交易转让
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\非交易转让 数据准备')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST{} where EXCHID = '1' and REGID in( '0117212000','0117212001','0117252000','0117252001')" \
                      " and STKID in ('159919','190180','190181') and DESKID = '077011'".format(year)
        exchangerights_sql = "select * FROM exchangerights  where exchid='1' and stkid in ('159919','190180','190181') " \
                             "and DESKID ='077011' and REGID in( '0117212000','0117212001','0117252000','0117252001')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         " stkid in ('159919','190180','190181') and briefid in('005_003_025','005_004_025'," \
                         "'005_005_076')".format(year, begintime, endtime)
        # 获取数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 获取excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist2022'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2022'))
        # 忽略字段
        stklist_ignore = ()
        exchangerights_ignore = ()
        tradinglog_ignore = ()
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog')
        # 断言
        final_result = stklist_result + exchangerights_result + tradinglog_result
        if not final_result:
            logger().info('深A\非交易转让 数据对比无异常')
            assert True
        else:
            logger().error('深A\非交易转让 数据对比异常:{}'.format(final_result))
            assert False, final_result


if __name__ == '__main__':
    unittest.main()