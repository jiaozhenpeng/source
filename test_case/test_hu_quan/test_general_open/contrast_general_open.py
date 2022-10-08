import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralOpen(unittest.TestCase):
    '''
    对比 沪权\普通开仓
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())

    def test_test_general_opening(self):
        '''
        对比 沪权\普通开仓
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 沪权\普通开仓 数据')
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        test_yaml = ContrastGeneralOpen().yaml['GeneralOpen']
        excel_path = test_yaml['excelPath']
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        # 查询SQL
        futureposition_sql = "select * from futureposition{} WHERE regid='A117212005'  and occurtime={} " \
                             "and stkid in('10002851','10002833','10002845','10002846')".format(year, begintime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid='A117212005'  and occurtime={} " \
                                   "and stkid in('10002851','10002833','10002845','10002846')".format(year, begintime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} " \
                               "and exchid='F' and regid='A117212005' and stkid in('10002851','10002833','10002845'," \
                               "'10002846')".format(year, begintime, endtime)
        # 忽略的字段
        futureposition_ignore = ('OCCURTIME',)
        futurepositiondetail_ignore = ('OCCURTIME','CLOSEKNOCKTIME','KNOCKTIME','OPTTIME')
        futuretradinglog_ignore = ('RECKONINGTIME', 'OCCURTIME', 'KNOCKTIME','POSTAMT','OPENDATE','SERIALNUM')
        # 获取数据库数据并排序
        futureposition_database = BaseAction().futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = BaseAction().futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取excel数据并排序
        futureposition_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition'))
        futurepositiondetail_excel = BaseAction().futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
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
            logger().info('沪权\普通开仓 对比数据无异常')
            assert True
        else:
            logger().error('沪权\普通开仓 对比数据异常')
            assert False, futureposition_result + futurepositiondetail_result + futuretradinglog_result
if __name__ == '__main__':
    unittest.main()