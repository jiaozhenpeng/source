import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastFuturesOpen(unittest.TestCase):
    """
    期货市场\冲抵保证金
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_futures_opening(self):
        """
        期货市场\冲抵保证金
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：期货市场\冲抵保证金')
        test_yaml = ContrastFuturesOpen().yaml['OffsetMargin']
        excel_path = test_yaml['excelPath']
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        occurtime = oracle.get_last_update()
        # 查询数据库SQL
        FutureClientCapitalDetail_sql = "select * from FutureClientCapitalDetail{} WHERE  occurtime = {} and " \
                                        "PARTICIPANTID='11721010' and  CASHID in('A004','A005')".format(year, occurtime)

        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={}" \
                               " and briefid in('205_003_036','205_003_037')".format(year, begintime, endtime)
        # 需要忽略的字段
        FutureClientCapitalDetail_ignore = self.ignore['FutureClientCapitalDetail']
        futuretradinglog_ignore = self.ignore['futuretradinglog']
        # 获取数据库数据并排序
        FutureClientCapitalDetail_database = BaseAction().FutureClientCapitalDetail_sort(oracle.dict_data(FutureClientCapitalDetail_sql))
        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取Excel数据并排序
        FutureClientCapitalDetail_excel = BaseAction().FutureClientCapitalDetail_sort(excel.read_excel('FutureClientCapitalDetail'))
        futuretradinglog_excel = BaseAction().futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        # 对比数据
        FutureClientCapitalDetail_result = BaseAction().compare_dict(FutureClientCapitalDetail_database, FutureClientCapitalDetail_excel,
                                                          'FutureClientCapitalDetail', *(FutureClientCapitalDetail_ignore))
        futuretradinglog_result = BaseAction().compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                            'futuretradinglog', *(futuretradinglog_ignore))
        final_result = FutureClientCapitalDetail_result + futuretradinglog_result
        if not final_result:
            logger().info('期货市场\冲抵保证金无异常')
            assert True
        else:
            logger().error('期货市场\冲抵保证金异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
