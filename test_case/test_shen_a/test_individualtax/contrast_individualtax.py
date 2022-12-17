import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    深A\股息红利税
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['individualtax']

    def test_restricted_shares(self):
        """
        深A\股息红利税
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\股息红利税 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1'  " \
                         "and  briefid in('005_005_059')".format(year, begintime, endtime)
        individualdividendtax_sql = "select * from individualdividendtax where  exchid ='1' "
        individualdividendtaxhis_sql = "select * from individualdividendtax{} where  exchid ='1' " \
                                       "and occurtime={}".format(year, begintime)
        # 数据库数据
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        individualdividendtax_database = base.individualdividendtax_sort(oracle.dict_data(individualdividendtax_sql))
        individualdividendtaxhis_database = base.individualdividendtax_sort(
            oracle.dict_data(individualdividendtaxhis_sql))
        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        individualdividendtax_excel = base.individualdividendtax_sort(excel.read_excel('individualdividendtax'))
        individualdividendtaxhis_excel = base.individualdividendtax_sort(excel.read_excel('individualdividendtax2022'))
        # 忽略字段
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
        'POSTAMT')
        individualdividendtaxhis_ignore = (
        'OCCURTIME', 'IMPTIME', 'MESSAGEDATE', 'DATE2', 'SENDDATE', 'RETURNDATE')
        individualdividendtax_ignore = ('IMPTIME', 'MESSAGEDATE', 'DATE2', 'SENDDATE', 'RETURNDATE')

        # 对比

        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        individualdividendtax_result = base.compare_dict(individualdividendtax_database, individualdividendtax_excel,
                                                         'individualdividendtax', *individualdividendtax_ignore)
        individualdividendtaxhis_result = base.compare_dict(individualdividendtaxhis_database,
                                                            individualdividendtaxhis_excel,
                                                            'individualdividendtax2022',
                                                            *individualdividendtaxhis_ignore)
        # 断言
        final_result = tradinglog_result + individualdividendtax_result + individualdividendtaxhis_result

        if not final_result:
            logger().info('深A\股息红利税 对比数据无异常')
            assert True
        else:
            logger().error('深A\股息红利税 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()