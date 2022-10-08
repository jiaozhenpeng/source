import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralLiquidation(unittest.TestCase):
    """
    沪权\普通平仓
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['GeneralLiquidation']

    def test_general_liquid(self):
        """
        沪权\普通平仓
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\普通平仓 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[0:4]
        # 查询SQL
        stkoptionsettlement_sql = "select * from stkoptionsettlement{}  where reckoningtime>={} and reckoningtime<={} " \
                                  "and exchid='X'  and stkid in('10002692','10002767','10002690','10002726')" \
                                  "and regid='A117212005' ".format(year, begintime, endtime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and " \
                               "exchid='X' and regid='A117212005' and stkid in('10002692','10002767','10002690'," \
                               "'10002726')".format(year, begintime, endtime)
        futureposition_sql = "select * from futureposition{} WHERE regid='A117212005'  and occurtime={} and stkid " \
                             "in('10002692','10002767','10002690','10002726')".format(year, begintime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid='A117212005'  and occurtime={} " \
                                   "and stkid in('10002692','10002767','10002690','10002726')".format(year, begintime)
        # 获取数据库数据
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        stkoptionsettlement_database = base.stkoptionsettlement_sort(oracle.dict_data(stkoptionsettlement_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        # excel 数据
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        stkoptionsettlement_excel = base.stkoptionsettlement_sort(excel.read_excel('stkoptionsettlement'))
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
        # 忽略字段
        futuretradinglog_ignore = ()
        stkoptionsettlement_ignore = ()
        futureposition_ignore = ()
        futurepositiondetail_ignore = ()
        # 对比结果
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog')
        stkoptionsettlement_result = base.compare_dict(stkoptionsettlement_database, stkoptionsettlement_excel,
                                                       'stkoptionsettlement')
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition')
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        # 断言
        final_result = futuretradinglog_result + stkoptionsettlement_result + futureposition_result + futurepositiondetail_result

        if not final_result:
            logger().info('沪权\普通平仓 对比数据无异常')
            assert True
        else:
            logger().error('沪权\普通平仓 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
