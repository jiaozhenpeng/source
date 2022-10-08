import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastFuturesOpen(unittest.TestCase):
    """
    期货市场\D市场交易数据\期货开仓 对比数据
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())

    def test_futures_opening(self):
        """
        期货市场\D市场交易数据\期货开仓
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：期货市场\D市场交易数据\期货开仓 对比数据')
        test_yaml = ContrastFuturesOpen().yaml['market_d']['FuturesOpen']
        excel_path = test_yaml['excelPath']
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        occurtime = oracle.get_last_update()
        # 查询数据库SQL
        futureposition_sql = "select * from futureposition{} WHERE regid='02767193'  and occurtime={} and stkid in('c2003'," \
                             "'eg2002','eg2003','fb1905','fb1906','fb1907','fb1908','fb1909','fb1910','fb1911','fb1912'," \
                             "'fb2001','fb2002','fb2003')".format(
            year, occurtime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid='02767193'  and occurtime={} and stkid in('c2003'," \
                                   "'eg2002','eg2003','fb1905','fb1906','fb1907','fb1908','fb1909','fb1910','fb1911','fb1912'," \
                                   "'fb2001','fb2002','fb2003')".format(
            year, occurtime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and exchid='D' and regid='02767193' and stkid in('c2003'," \
                               "'eg2002','eg2003','fb1905','fb1906','fb1907','fb1908','fb1909','fb1910','fb1911','fb1912'," \
                               "'fb2001','fb2002','fb2003')".format(
            year, begintime, endtime)
        # 需要忽略的字段
        futureposition_ignore = ('OCCURTIME',)
        futurepositiondetail_ignore = ('OCCURTIME','CLOSEKNOCKTIME','KNOCKTIME','OPTTIME')
        futuretradinglog_ignore = ('RECKONINGTIME', 'OCCURTIME', 'KNOCKTIME','POSTAMT','OPENDATE','SERIALNUM')
        # 获取数据库数据并排序
        futureposition_database = BaseAction().futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = BaseAction().futurepositiondetail_sort(
            oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取Excel数据并排序
        futureposition_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition2021'))
        futurepositiondetail_excel = BaseAction().futurepositiondetail_sort(
            excel.read_excel('futurepositiondetail2021'))
        futuretradinglog_excel = BaseAction().futuretradinglog_sort(excel.read_excel('futuretradinglog2021'))
        # 对比数据
        futureposition_result = BaseAction().compare_dict(futureposition_database, futureposition_excel,
                                                          'futureposition', *(futureposition_ignore))
        futurepositiondetail_result = BaseAction().compare_dict(futurepositiondetail_database,
                                                                futurepositiondetail_excel, 'futurepositiondetail',
                                                                *(futurepositiondetail_ignore))
        futuretradinglog_result = BaseAction().compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                            'futuretradinglog', *(futuretradinglog_ignore))
        if not futureposition_result and not futurepositiondetail_result and not futuretradinglog_result:
            logger().info('期货市场\D市场交易数据\期货开仓 对比数据无异常')
            assert True
        else:
            logger().error('期货市场\D市场交易数据\期货开仓 对比数据异常')
            assert False, futureposition_result + futurepositiondetail_result + futuretradinglog_result


if __name__ == '__main__':
    unittest.main()
