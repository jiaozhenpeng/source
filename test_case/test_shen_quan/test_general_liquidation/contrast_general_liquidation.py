import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralLiquidation(unittest.TestCase):
    """
    深权\普通平仓
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_quan())['GeneralLiquidation']

    def test_general_liquidation(self):
        """
        深权\普通平仓
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深权\普通平仓 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        futureposition_sql = "select * from futureposition WHERE regid='0117212005' and exchid = 'Y'  and stkid" \
                             " in('90005420','90005421','90005424','90005425','90005465','90005466'," \
                             "'90005469','90005470','90005456','90005457','90005438','90005439','90005442'," \
                             "'90005443','90005447','90005448','90005451','90005452','90005461'," \
                             "'90005462') and DESKID='077011'"
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and" \
                               " exchid='Y' and regid in('0117212005','A117212005') and stkid in('90005437'," \
                               "'90005438','90005439','90005440','90005441','90005442','90005443','90005444'," \
                               "'90005446','90005447','90005448','90005449','90005450','90005451','90005452'," \
                               "'90005453','90005460','90005461','90005462'," \
                               "'90005463','90005419','90005420','90005421','90005422','90005423','90005424'," \
                               "'90005425','90005464','90005465','90005466','90005467','90005468','90005469'," \
                               "'90005470','90005471','90005455','90005456','90005457','90005458','90005426'," \
                               "'10002845','10002846','90000501','90000504')".format(year, begintime, endtime)
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE regid='0117212005' and exchid ='Y'and stkid" \
                                   " in('90005420','90005421','90005424','90005425','90005465','90005466'," \
                                   "'90005469','90005470','90005456','90005457','90005438','90005439','90005442'," \
                                   "'90005443','90005447','90005448','90005451','90005452','90005461','90005462') and" \
                                   " DESKID='077011'"
        # 数据库数据
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        # Excel数据
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog2021'))
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
        # 忽略字段
        futureposition_ignore = ()
        futuretradinglog_ignore = ()
        futurepositiondetail_ignore = ()
        # 对比
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition')
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog')
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        # 断言
        final_result = futureposition_result + futuretradinglog_result + futurepositiondetail_result
        if not final_result:
            logger().info('深权\普通平仓 对比数据无异常')
            assert True
        else:
            logger().error('深权\普通平仓 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
