import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深A\限售股所得税
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['SZSDS']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深A\限售股所得税
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\限售股所得税 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        # 查询SQL
        CustSellLimitTax_sql = "select * from   CustSellLimitTax where knocktime={} and offerregid in('0117212000','0117252000') ".format(begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and" \
                         "  regid in ('0117212000','0117252000') and briefid = '005_005_030'".format(year, begintime, endtime)
        # 查询数据库
        # print(oracle.dict_data(CustSellLimitTax_sql))
        CustSellLimitTax_database = base.CustSellLimitTax_sort(oracle.dict_data(CustSellLimitTax_sql))
        tradinglog_database = base.tradinglog_sort4(oracle.dict_data(tradinglog_sql))
        # 查询excel
        CustSellLimitTax_excel = base.CustSellLimitTax_sort(excel.read_excel('CustSellLimitTax'))
        tradinglog_excel = base.tradinglog_sort4(excel.read_excel('tradinglog'))
        # 忽略字段
        CustSellLimitTax_ignore = ('OCCURTIME','KNOCKTIME','SERIALNUM','POSTDATE','BRIEFIDLIST')
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
            'POSTAMT','NOTENUM')
        # 对比结果
        CustSellLimitTax_result = base.compare_dict(CustSellLimitTax_database,CustSellLimitTax_excel,'CustSellLimitTax',*CustSellLimitTax_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
      # 断言
        final_result =  tradinglog_result + CustSellLimitTax_result
        if not final_result:
            logger().info('深A\限售股所得税 对比数据无异常')
            assert True
        else:
            logger().error('深A\限售股所得税 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
