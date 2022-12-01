import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralOpenShen(unittest.TestCase):
    '''
    深权\分配虚拟股东
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_quan())['virtualregistrationrights']

    def test_general_opening(self):
        '''
        对比深权\分配虚拟股东
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 深权\分配虚拟股东 数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        # 查询SQL
        futureposition_sql = "select * from futureposition WHERE exchid='Y'  AND stkid  " \
                             " in('90001180','90001181','90001182','90001183')"
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE stkid in('90001180','90001181'," \
                                   "'90001182','90001183') and EXCHID = 'Y'"
        futurepositionhis_sql = "select * from futureposition{} WHERE   occurtime={} and stkid in('90001180'," \
                                "'90001181','90001182','90001183') and EXCHID = 'Y'".format(year, begintime)
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} " \
                               "and exchid='Y'  and stkid in('90001180','90001181','90001182','90001183')".format(year, begintime, endtime)
        # 忽略的字段
        futurepositiondetail_ignore = ( 'CLOSEKNOCKTIME', 'KNOCKTIME', 'OPTTIME')
        futuretradinglog_ignore = ('RECKONINGTIME', 'OCCURTIME', 'KNOCKTIME', 'POSTAMT', 'OPENDATE', 'SERIALNUM')
        uturepositionhis_ignore = ('OCCURTIME',)
        # 获取数据库数据并排序
        futureposition_database = BaseAction().futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = BaseAction().futurepositiondetail_sort(
            oracle.dict_data(futurepositiondetail_sql))
        futurepositionhis_database = BaseAction().futureposition_sort(oracle.dict_data(futurepositionhis_sql))

        futuretradinglog_database = BaseAction().futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        # 获取excel数据并排序
        futureposition_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition'))
        futurepositiondetail_excel = BaseAction().futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
        futurepositionhis_excel = BaseAction().futureposition_sort(excel.read_excel('futureposition2022'))
        futuretradinglog_excel = BaseAction().futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        # 对比数据
        futureposition_result = BaseAction().compare_dict(futureposition_database, futureposition_excel,'futureposition')
        futurepositiondetail_result = BaseAction().compare_dict(futurepositiondetail_database,futurepositiondetail_excel,
                                                                'futurepositiondetail',*futurepositiondetail_ignore)
        futurepositionhis_result = BaseAction().compare_dict(futurepositionhis_database, futurepositionhis_excel,
                                                             'futurepositionhis',*uturepositionhis_ignore)
        futuretradinglog_result = BaseAction().compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                            'futuretradinglog',*futuretradinglog_ignore)
        end_result = futureposition_result + futurepositiondetail_result +  futuretradinglog_result + futurepositionhis_result
        if not end_result:
            logger().info('深权\分配虚拟股东 对比数据无异常')
            assert True
        else:
            logger().error('深权\分配虚拟股东 对比数据异常')
            assert False, end_result

if __name__ == '__main__':
    unittest.main()