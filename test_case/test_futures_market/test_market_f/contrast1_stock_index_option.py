import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastStockIndexOption(unittest.TestCase):
    """
    F市场\股指期权\T+1日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['MarketF']['StockIndexOption']

    def test_stock_index_option(self):
        """
        F市场\股指期权\T+1日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：F市场\股指期权\T+1日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        futureposition_sql = "select * from futureposition{} WHERE regid in ('00058049','F1008666','00888886') and" \
                             " occurtime={} and stkid in('IO2107-C-4600','IO2107-C-4550','IO2108-P-4650','IO2108-C-4650','IO2107-C-4900','IO2107-C-4700','IO2107-C-4500','IO2108-P-4700','IO2108-C-4600','IO2107-C-5000','IO2107-C-4450','IO2108-C-4850','IO2107-C-5900','IO2107-P-4450','IO2107-C-5800','IO2108-C-4900','IO2107-P-4650','IO2107-P-4600','IO2107-P-4500','IO2107-P-4550') and exchid = 'F'".format(
            year, begintime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid in ('00058049','F1008666','00888886')" \
                                   "  and occurtime={} and stkid in('IO2107-C-4600','IO2107-C-4550','IO2108-P-4650'," \
                                   "'IO2108-C-4650','IO2107-C-4900','IO2107-C-4700','IO2107-C-4500','IO2108-P-4700'," \
                                   "'IO2108-C-4600','IO2107-C-5000','IO2107-C-4450','IO2108-C-4850','IO2107-C-5900'," \
                                   "'IO2107-P-4450','IO2107-C-5800','IO2108-C-4900','IO2107-P-4650','IO2107-P-4600'," \
                                   "'IO2107-P-4500','IO2107-P-4550') and exchid = 'F'".format(year, begintime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and" \
                               " exchid='F' and regid in ('00058049','F1008666','00888886') and stkid in('IO2107-C-4600'," \
                               "'IO2107-C-4550','IO2108-P-4650','IO2108-C-4650','IO2107-C-4900','IO2107-C-4700'," \
                               "'IO2107-C-4500','IO2108-P-4700','IO2108-C-4600','IO2107-C-5000','IO2107-C-4450'," \
                               "'IO2108-C-4850','IO2107-C-5900','IO2107-P-4450','IO2107-C-5800','IO2108-C-4900'," \
                               "'IO2107-P-4650','IO2107-P-4600','IO2107-P-4500','IO2107-P-4550'" \
                               ")".format(year,begintime,endtime)
        # 数据库数据
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        # Excel数据
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail2021'))
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition2021'))
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        # 忽略字段
        futurepositiondetail_ignore = ()
        futureposition_ignore = ('OCCURTIME',)
        futuretradinglog_ignore = ()
        # 对比结果
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition',
                                                  *(futureposition_ignore))
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog')
        # 断言
        final_result = futureposition_result + futurepositiondetail_result + futuretradinglog_result

        if not final_result:
            logger().info('F市场\股指期权\T+1日 对比数据无异常')
            assert True
        else:
            logger().error('F市场\股指期权\T+1日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
