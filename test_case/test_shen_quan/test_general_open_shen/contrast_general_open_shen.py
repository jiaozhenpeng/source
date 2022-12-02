import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralOpenShen(unittest.TestCase):
    '''
    深权\普通开仓
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_quan())['GeneralOpenShen']

    def test_general_opening(self):
        '''
        对比深权\普通开仓
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 深权\普通开仓 数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        # 查询SQL
        futureposition_sql = "select * from futureposition{} WHERE regid='0117212005'  and occurtime={} " \
                             "and stkid in('90000500','90000501','90000503','90000504','90000511','90000512') " \
                             "and EXCHID = 'Y'".format(year, begintime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid='0117212005'  and occurtime={} " \
                                   "and stkid in('90000500','90000501','90000503','90000504','90000511','90000512') \
                                   and EXCHID = 'Y'".format(year, begintime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} " \
                               "and exchid='Y' and regid='0117212005' and stkid in('90000500','90000501','90000503'," \
                               "'90000504','90000511','90000512')".format(year, begintime, endtime)
        # 忽略的字段
        futureposition_ignore = ('OCCURTIME',)
        futurepositiondetail_ignore = ('OCCURTIME', 'CLOSEKNOCKTIME', 'KNOCKTIME', 'OPTTIME')
        futuretradinglog_ignore = ('RECKONINGTIME', 'OCCURTIME', 'KNOCKTIME', 'POSTAMT', 'OPENDATE', 'SERIALNUM')
        # 获取数据库数据并排序
        futureposition_database = BaseAction().futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = BaseAction().futurepositiondetail_sort(
            oracle.dict_data(futurepositiondetail_sql))
        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取excel数据并排序
        futureposition_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition2021'))
        futurepositiondetail_excel = BaseAction().futurepositiondetail_sort(
            excel.read_excel('futurepositiondetail2021'))
        futuretradinglog_excel = BaseAction().futuretradinglog_sort(excel.read_excel('futuretradinglog2021'))
        # 对比数据
        futureposition_result = BaseAction().compare_dict(futureposition_database, futureposition_excel,
                                                          'futureposition',*futureposition_ignore)
        futurepositiondetail_result = BaseAction().compare_dict(futurepositiondetail_database,
                                                                futurepositiondetail_excel,'futurepositiondetail',
                                                                *futurepositiondetail_ignore)
        futuretradinglog_result = BaseAction().compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                            'futuretradinglog',*futuretradinglog_ignore)
        end_result = futureposition_result + futurepositiondetail_result  + futuretradinglog_result
        if not end_result:
            logger().info('深权\普通开仓 对比数据无异常')
            assert True
        else:
            logger().error('深权\普通开仓 对比数据异常')
            assert False, end_result

if __name__ == '__main__':
    unittest.main()