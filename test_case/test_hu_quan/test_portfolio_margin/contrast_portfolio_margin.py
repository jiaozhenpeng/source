import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastPortfolioMargin(unittest.TestCase):
    """
    沪权\组合保证金
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['PortfolioMargin']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_portfolio_margin(self):
        """
        沪权\组合保证金
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\组合保证金 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        futurecombaction_sql = "select * from futurecombaction where EXCHID = 'X' and REGID = 'A117212005' and " \
                               "STKID in ('10003693','10003951','10003840','10003958','10003964','10003963','10003997'," \
                               "'10004033','10004106','10004105','10004024','10003893') and DESKID = '00W40'"
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and " \
                               "exchid='X' and regid='A117212005' and stkid in('10003693','10003951','10003840'," \
                               "'10003958','10003964','10003963','10003997','10004033','10004106','10004105'," \
                               "'10004024','10003893')".format(year, begintime, endtime)
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE regid='A117212005'  and stkid in" \
                                   "('10003693','10003951','10003840','10003958','10003964','10003963','10003997'," \
                                   "'10004033','10004106','10004105','10004024','10003893') and exchid = 'X'"

        futureposition_sql = "select * from futureposition where EXCHID = 'X' and REGID = 'A117212005' and " \
                             "STKID in ('10003693','10003951','10003840','10003958','10003964','10003963','10003997'," \
                             "'10004033','10004106','10004105','10004024','10003893') and DESKID = '00W40'"
        # 数据库数据
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futurecombaction_database = base.futurecombaction_sort(oracle.dict_data(futurecombaction_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))

        # excel数据
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        futurecombaction_excel = base.futurecombaction_sort(excel.read_excel('futurecombaction'))
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        # 忽略字段
        futureposition_ignore = ('OCCURTIME',)
        futurecombaction_ignore = ()
        futurepositiondetail_ignore = self.ignore['futurecombaction']
        futuretradinglog_ignore = self.ignore['futuretradinglog']
        stkoptionsettlement_ignore = ()
        # 排序
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition')
        futurecombaction_result = base.compare_dict(futurecombaction_database, futurecombaction_excel,
                                                    'futurecombaction')
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog',*futuretradinglog_ignore)

        final_result = futureposition_result + futurecombaction_result + futurepositiondetail_result + \
                       futuretradinglog_result

        if not final_result:
            logger().info('沪权\组合保证金 对比数据无异常')
            assert True
        else:
            logger().error('沪权\组合保证金 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()