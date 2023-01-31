import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastFuturesOpen(unittest.TestCase):
    """
    广期所\智能开平账户开仓 对比数据
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_futures_opening(self):
        """
        广期所\智能开平账户开仓
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：广期所\智能开平账户开仓 对比数据')
        test_yaml = ContrastFuturesOpen().yaml['intelligent']['open']
        excel_path = test_yaml['excelPath']
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        occurtime = oracle.get_last_update()
        # 查询数据库SQL
        futureposition_sql = "select * from futureposition WHERE offerregid in('G00777','G00666')  and exchid='G' and stkid='si2303' "
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE offerregid in('G00777','G00666')  " \
                                   "and exchid='G' and stkid='si2303'"
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} " \
                               " and regid in('G00666','G2777777')  and briefid in('205_001_001','205_001_002') and exchid='G' and stkid='si2303' ".format(
            year, begintime, endtime)
        # 需要忽略的字段
        futureposition_ignore = self.ignore['futureposition']
        futurepositiondetail_ignore = self.ignore['futurepositiondetail']
        futuretradinglog_ignore = self.ignore['futuretradinglog']
        # 获取数据库数据并排序
        futureposition_database = BaseAction().futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = BaseAction().futurepositiondetail_sort(
            oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取Excel数据并排序
        futureposition_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition'))
        futurepositiondetail_excel = BaseAction().futurepositiondetail_sort(
            excel.read_excel('futurepositiondetail'))
        futuretradinglog_excel = BaseAction().futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        # 对比数据
        futureposition_result = BaseAction().compare_dict(futureposition_database, futureposition_excel,
                                                          'futureposition', *(futureposition_ignore))
        futurepositiondetail_result = BaseAction().compare_dict(futurepositiondetail_database,
                                                                futurepositiondetail_excel, 'futurepositiondetail',
                                                                *(futurepositiondetail_ignore))
        futuretradinglog_result = BaseAction().compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                            'futuretradinglog', *(futuretradinglog_ignore))
        if not futureposition_result and not futurepositiondetail_result and not futuretradinglog_result:
            logger().info('广期所\智能开平账户开仓 对比数据无异常')
            assert True
        else:
            logger().error('广期所\智能开平账户开仓 对比数据异常')
            assert False, futureposition_result + futurepositiondetail_result + futuretradinglog_result


if __name__ == '__main__':
    unittest.main()
