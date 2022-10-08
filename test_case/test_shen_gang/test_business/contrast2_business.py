import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class Contrast2Business(unittest.TestCase):
    """
    深港\\买卖T+2日清算
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_gang())['Business']

    def test_shen_business(self):
        logger().info('-------------------------------')
        logger().info('开始执行：深港\\买卖T+2日清算 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '4' and REGID in( '0117222000','0117222001') and STKID " \
                      "in ('00476','23131','01217') and DESKID = '077011'"
        unprocessedreckoningresult_sql = "select * from unprocessedreckoningresult where STKID in " \
                                         "('00476','23131','01217') and DESKID = '077011' and EXCHID = '4' and " \
                                         "REGID in( '0117222000','0117222001')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '4'" \
                         " and  acctid in ('000011722200','000011722201') and briefid in('005_001_001','005_002_001')".format(
            year, begintime, endtime)
        # 需要忽略的字段
        stklist_ignore = ()
        tradinglog_ignore =  ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE','TRANSACTIONREF')
        # 获取数据库数据并排序
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = BaseAction().tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 获取excel数据并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = BaseAction().tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 对比数据
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
        unprocessedreckoningresult_result = oracle.select_sql(unprocessedreckoningresult_sql)[0] # 清算T+2日时此表数据为空
        if not stklist_result and not tradinglog_result and not unprocessedreckoningresult_result:
            logger().info('深港\\买卖T+2日清算 对比数据无异常')
            assert True
        elif unprocessedreckoningresult_result:
            logger().error('unprocessedreckoningresult非空，预期为空')
            assert False,'unprocessedreckoningresult非空，预期为空'
        else:
            logger().error('深港\\买卖T+2日清算 对比数据异常')
            assert False, stklist_result + unprocessedreckoningresult_result

if __name__ == '__main__':
    unittest.main()
