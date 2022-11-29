import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastIncomeTax(unittest.TestCase):
    """
    对比 股转\所得税
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['IncomeTax']['incomeTax']

    def test_incomt_tax(self):
        """
        对比 股转\所得税
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 股转\所得税 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        CustSellLimitTax_sql = "select * from   CustSellLimitTax where knocktime={} and offerregid='GZ11721600' ".format(begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' and" \
                         "  regid in ('GZ11721600','GZ11721601') and briefid = '005_005_030'".format(year, begintime, endtime)
        # 查询数据库
        # print(oracle.dict_data(CustSellLimitTax_sql))
        CustSellLimitTax_database = base.CustSellLimitTax_sort(oracle.dict_data(CustSellLimitTax_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # 查询excel
        CustSellLimitTax_excel = base.CustSellLimitTax_sort(excel.read_excel('CustSellLimitTax'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 忽略字段
        CustSellLimitTax_ignore = ('OCCURTIME','KNOCKTIME','SERIALNUM')
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
            'POSTAMT')
        # 对比结果
        CustSellLimitTax_result = base.compare_dict(CustSellLimitTax_database,CustSellLimitTax_excel,'CustSellLimitTax',*CustSellLimitTax_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
        # 断言
        final_result = CustSellLimitTax_result + tradinglog_result
        if not final_result:
            logger().info('股转\所得税 数据对比无异常')
            assert True
        else:
            logger().error('股转\所得税 数据对比异常:{}'.format(final_result))
            assert False, final_result

if __name__ == '__main__':
    unittest.main()

