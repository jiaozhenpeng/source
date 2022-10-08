import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastReserveExercise(unittest.TestCase):
    """
    沪权\备兑后行权
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['ReserveExercise']

    def test_reserve_exercise(self):
        """
        沪权\备兑后行权
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\备兑后行权 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        futureposition_sql = "select * from futureposition WHERE regid='A117212005'  and " \
                             "stkid ='10003527' and exchid = 'X'"
        stkoptionsettlement_sql = "select * from stkoptionsettlement  where reckoningtime>={} and reckoningtime<={} " \
                                  "and exchid='X' and regid='A117212005' and stkid ='10003527' ".format(begintime,
                                                                                                        endtime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and " \
                               "exchid='X' and regid='A117212005' and stkid ='10003527'".format(year, begintime,
                                                                                                endtime)
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE regid='A117212005'  and occurtime={} and " \
                                   "stkid ='10003527' and exchid = 'X'".format(begintime)
        # 数据库数据
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        stkoptionsettlement_database = base.stkoptionsettlement_sort(oracle.dict_data(stkoptionsettlement_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        # excel数据
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
        stkoptionsettlement_excel = base.stkoptionsettlement_sort(excel.read_excel('stkoptionsettlement'))
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        # 忽略字段
        futuretradinglog_ignore = ()
        futurepositiondetail_ignore = ()
        stkoptionsettlement_ignore = ()
        futureposition_ignore = ()
        # 对比数据
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog')
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        stkoptionsettlement_result = base.compare_dict(stkoptionsettlement_database, stkoptionsettlement_excel,
                                                       'stkoptionsettlement')
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition')
        final_result = futuretradinglog_result + futurepositiondetail_result + stkoptionsettlement_result + futureposition_result
        if not final_result:
            logger().info('沪权\备兑后行权 对比数据无异常')
            assert True
        else:
            logger().error('沪权\备兑后行权 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()