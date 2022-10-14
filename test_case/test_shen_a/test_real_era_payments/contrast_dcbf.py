import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class DESY(unittest.TestCase):
    """
    深A\实时代收付\CDS业务保费支付
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['RealEraPayments']['DCBF']

    def test_DESY(self):
        """
        深A\实时代收付\CDS业务保费支付
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\实时代收付\CDS业务保费支付 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         " regid in ('0117252000','0117212000') and " \
                         "briefid in( '005_005_092','005_005_091')".format(year, begintime, endtime)        # 数据库数据
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        # 忽略字段
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME',
                             'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF', 'POSTAMT')
        # 对比
        tradinglog_result = base.compare_dict(tradinglog_database,tradinglog_excel,
                                                      'tradinglog',*tradinglog_ignore)
        # 断言
        final_result = tradinglog_result
        if not final_result:
            logger().info('深A\实时代收付\CDS业务保费支付 对比数据无异常')
            assert True
        else:
            logger().error('深A\实时代收付\CDS业务保费支付 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
