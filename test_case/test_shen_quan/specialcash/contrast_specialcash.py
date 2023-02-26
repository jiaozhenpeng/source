import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    特殊资金自动上账
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_quan())['specialcash']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        特殊资金自动上账
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：特殊资金自动上账 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        futuretradinglog_sql = "select * from futuretradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= 'Y'  " \
                         "and briefid in ('208_002_042','208_002_041') ".format(year, begintime, endtime)
        account_sql = "select * from account where  acctid='000000001215' and currencyid='00'"

        # 数据库数据
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        account_database = base.account_sort(oracle.dict_data(account_sql))

        # Excel数据
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        account_excel = base.account_sort(excel.read_excel('account'))
        # 忽略字段
        futuretradinglog_ignore = self.ignore['futuretradinglog']
        # 对比

        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel, 'futuretradinglog', *futuretradinglog_ignore)
        account_result = base.compare_dict(account_database,account_excel,'account')
        # 断言
        final_result =   futuretradinglog_result + account_result
        if not (final_result ):
            logger().info('特殊资金自动上账 对比数据无异常')
            assert True
        else:
            logger().error('特殊资金自动上账 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
