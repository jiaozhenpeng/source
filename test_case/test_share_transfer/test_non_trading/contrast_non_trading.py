import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastNonTrading(unittest.TestCase):
    """
    对比 股转\股份非交易过户
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['NonTrading']

    def test_non_transaction_transfer(self):
        """
        对比 股转\股份非交易过户
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 股转\股份非交易过户 数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        year = BaseAction().get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID in( 'GZ11721600','GZ11721601') and STKID in " \
                      "('810005','810006') and DESKID = 'ANQ001'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' " \
                         " and briefid in('005_003_025','005_004_025') and stkid in" \
                         " ('810005','810006')".format(year, begintime, endtime)
        # 获取数据库数据并排序
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = BaseAction().tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 获取excel数据并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = BaseAction().tradinglog_sort(excel.read_excel('tradinglog'))
        # 忽略字段
        stklist_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        # 对比数据
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog',
                                                      *tradinglog_ignore)
        # 判断数据
        final_result = stklist_result + tradinglog_result
        if not final_result:
            logger().info('股转\股份非交易过户 数据对比无异常')
            assert True
        else:
            logger().error('股转\股份非交易过户 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
