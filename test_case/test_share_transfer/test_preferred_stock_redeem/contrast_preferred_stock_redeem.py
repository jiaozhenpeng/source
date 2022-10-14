import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation

class ContrastPreferredStockRedeem(unittest.TestCase):
    """
    股转\优先股赎回
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['PreferredStockRedeem']

    def test_reddem(self):
        """
        股转\优先股赎回
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 股转\优先股赎回 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID in( 'GZ11721600','GZ11721601')" \
                      " and STKID = '820003' and DESKID = 'ANQ001' "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' and " \
                         " stkid = '820003' and briefid in('005_005_005','005_004_004')".format(year, begintime, endtime)
        # 获取数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 获取excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 忽略字段
        stklist_ignore = ('OCCURTIME')
        exchangerights_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
            'POSTAMT')
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist',*stklist_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog',*tradinglog_ignore)
        # 断言
        final_result = stklist_result +  tradinglog_result
        if not final_result:
            logger().info('股转\优先股赎回 数据对比无异常')
            assert True
        else:
            logger().error('股转\优先股赎回 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()