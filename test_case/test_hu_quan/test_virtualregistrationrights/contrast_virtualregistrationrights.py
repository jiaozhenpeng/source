import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralOpenShen(unittest.TestCase):
    '''
    沪权\分配虚拟股东
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['virtualregistrationrights']

    def test_general_opening(self):
        '''
        对比沪权\分配虚拟股东
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 沪权\分配虚拟股东 数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        # 查询SQL
        futureposition_sql = "select * from futureposition WHERE exchid='X' and stkid IN('10004244','10004247'," \
                             "'10004246','10004245')"
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE exchid='X' and stkid IN('10004244'," \
                                   "'10004247','10004246','10004245')"
        futurepositionhis_sql = "select * from futureposition{} WHERE   occurtime={} and exchid='X' and stkid " \
                                "IN('10004244','10004247','10004246','10004245')".format(year, begintime)
        futurepositiondetailhis_sql = "select * from futurepositiondetail{} WHERE   occurtime={} and exchid='X' and stkid " \
                                      "IN('10004244','10004247','10004246','10004245')".format(year, begintime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} " \
                               "and exchid='X' and stkid IN('10004244','10004247','10004246','10004245')".format(year, begintime, endtime)
        # 忽略的字段
        futurepositiondetail_ignore = ( 'CLOSEKNOCKTIME', 'KNOCKTIME', 'OPTTIME')
        futuretradinglog_ignore = ('RECKONINGTIME', 'OCCURTIME', 'KNOCKTIME', 'POSTAMT', 'OPENDATE', 'SERIALNUM')
        futurepositionhis_ignore = ('OCCURTIME',)
        futurepositiondetailhis_ignore = ( 'OCCURTIME','CLOSEKNOCKTIME', 'KNOCKTIME', 'OPTTIME')

        # 获取数据库数据并排序
        futureposition_database = oracle.dict_data(futureposition_sql)
        futurepositiondetail_database = oracle.dict_data(futurepositiondetail_sql)
        futurepositionhis_database = BaseAction().futureposition_sort(oracle.dict_data(futurepositionhis_sql))
        futurepositiondetailhis_database = BaseAction().futurepositiondetail_sort(
            oracle.dict_data(futurepositiondetailhis_sql))
        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取excel数据并排序
        futurepositionhis_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition2022'))
        futurepositiondetailhis_excel = BaseAction().futurepositiondetail_sort(excel.read_excel('futurepositiondetail2022'))
        futuretradinglog_excel = BaseAction().futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        # 对比数据
        futurepositionhis_result = BaseAction().compare_dict(futurepositionhis_database, futurepositionhis_excel,
                                                             'futurepositionhis',*futurepositionhis_ignore)
        futurepositiondetailhis_result = BaseAction().compare_dict(futurepositiondetailhis_database, futurepositiondetailhis_excel,
                                                                   'futurepositiondetailhis',*futurepositiondetailhis_ignore)
        futuretradinglog_result = BaseAction().compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                            'futuretradinglog',*futuretradinglog_ignore)
        end_result =   futuretradinglog_result + futurepositionhis_result + futurepositiondetailhis_result\
                       + futureposition_database + futurepositiondetail_database  #当前表数据库查不到
        if not end_result:
            logger().info('沪权\分配虚拟股东 对比数据无异常')
            assert True
        else:
            logger().error('沪权\分配虚拟股东 对比数据异常')
            assert False, end_result

if __name__ == '__main__':
    unittest.main()