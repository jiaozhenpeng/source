import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastFutures(unittest.TestCase):
    """
    F市场\期货\T日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['MarketF']['Futures']

    def test_futures(self):
        """
        F市场\期货\T日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：F市场\期货\T日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        futuretraderslt_sql = "select * from futuretraderslt where exchid='F' and regid in ('00058049','F1008666'," \
                              "'00888886','00060447') and stkid in('IC2108','IC2109','IC2112','IF2108','IF2109','IF2112','IH2109','T2109','T2112','TF2112')"
        futureposition_sql = "select * from futureposition{} WHERE regid in ('00058049','F1008666','00888886','00060447') and" \
                             " occurtime={} and stkid in('IC2108','IC2109','IC2112','IF2108','IF2109','IF2112'," \
                             "'IH2109','T2109','T2112','TF2112') and exchid = 'F'".format(year, begintime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid in ('00058049','F1008666'," \
                                   "'00888886','00060447') and occurtime={} and stkid in('IC2108','IC2109','IC2112'," \
                                   "'IF2108','IF2109','IF2112','IH2109','T2109','T2112'," \
                                   "'TF2112') and exchid = 'F'".format(year, begintime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and" \
                               " exchid='F' and regid in ('00058049','F1008666','00888886','00060447') and stkid in" \
                               "('IC2108','IC2109','IC2112','IF2108','IF2109','IF2112','IH2109','T2109','T2112','TF2112'" \
                               ")".format(year, begintime, endtime)
        # 数据库数据
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futuretraderslt_database = base.futuretraderslt_sort(oracle.dict_data(futuretraderslt_sql))

        # Excel数据
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail2021'))
        futureposition_excel = base.futureposition_sort(excel.read_excel('fuutreposition2021'))
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog2021'))
        futuretraderslt_excel = base.futuretraderslt_sort(excel.read_excel('futuretraderslt'))

        # 忽略字段
        futurepositiondetail_ignore = ()
        futureposition_ignore = ('OCCURTIME',)
        futuretradinglog_ignore = ()
        futuretraderslt_ignore = ()

        # 对比结果
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition',
                                                  *(futureposition_ignore))
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog')
        futuretraderslt_result = base.compare_dict(futuretraderslt_database, futuretraderslt_excel, 'futuretraderslt')

        # 断言
        final_result = futureposition_result + futurepositiondetail_result + futuretradinglog_result + \
                       futuretraderslt_result



        if not final_result:
            logger().info('F市场\期货\T日 对比数据无异常')
            assert True
        else:
            logger().error('F市场\期货\T日 对比数据异常')
            assert False, final_result


