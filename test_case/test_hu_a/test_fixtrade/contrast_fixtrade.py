import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\指定交易
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['fixtrade']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪A\指定交易
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\指定交易 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        registration_sql = "select * from registration where exchid in('0','5','X','B') and offerregid in('0019910214','0019910216')"
        custchglog_sql = " select * from   custchglog{} where CHANGETIME>={}  and CHANGETIME<={} and   briefid" \
                         " in('006_003_020','006_003_019')".format(year,begintime,endtime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and briefid " \
                         "in('006_003_020','006_003_019') ".format(year, begintime, endtime)

        # 数据库数据
        registration_database = base.registration_sort(oracle.dict_data(registration_sql))
        custchglog_database = base.custchglog_sort(oracle.dict_data(custchglog_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        registration_excel = base.registration_sort(excel.read_excel('registration'))
        custchglog_excel = base.custchglog_sort(excel.read_excel('custchglog'))


        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        custchglog_ignore = self.ignore['custchglog']
        # 对比

        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        registration_result = base.compare_dict(registration_database, registration_excel, 'registration')
        custchglog_result = base.compare_dict(custchglog_database,custchglog_excel,'custchglog',*custchglog_ignore)

        # 断言
        final_result =   tradinglog_result + registration_result + custchglog_result
        if not final_result :
            logger().info('沪A\指定交易 对比数据无异常')
            assert True
        else:
            logger().error('沪A\指定交易 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
