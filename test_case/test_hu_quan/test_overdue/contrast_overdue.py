import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralLiquidation(unittest.TestCase):
    """
    沪权\过期
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['Overdue']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_general_liquid(self):
        """
        沪权\过期
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\过期 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[0:4]
        # 查询SQL

        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and " \
                               "exchid='X' and regid='A117212005' and stkid in('10002498','10002715')".format(year, begintime, endtime)
        futurepositionhis_sql = "select * from futureposition{} WHERE regid='A117212005'  and occurtime={} and stkid " \
                             "in('10002498','10002715')".format(year, begintime)
        futurepositiondetailhis_sql = "select * from futurepositiondetail{} WHERE regid='A117212005'  and occurtime={} " \
                                   "and stkid in('10002498','10002715')".format(year, begintime)
        futureposition_sql = "select * from futureposition WHERE regid='A117212005'   and stkid  in('10002498','10002715') "
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE regid='A117212005'   and stkid" \
                                   " in('10002498','10002715') "
        # 获取数据库数据
        futurepositiondetailhis_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetailhis_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futurepositionhis_database = base.futureposition_sort(oracle.dict_data(futurepositionhis_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        # excel 数据
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        futurepositionhis_excel = base.futureposition_sort(excel.read_excel('futureposition2023'))
        futurepositiondetailhis_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail2023'))
        # futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        # futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))

        # 忽略字段
        futuretradinglog_ignore = self.ignore['futuretradinglog']
        futurepositionhis_ignore = self.ignore['futurepositionhis']
        futurepositiondetail_ignore = self.ignore['futurepositiondetail']
        futurepositiondetailhis_ignore = self.ignore['futurepositiondetailhis']


        # 对比结果
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog',*futuretradinglog_ignore)
        futurepositionhis_result = base.compare_dict(futurepositionhis_database, futurepositionhis_excel,
                                                     'futureposition2022',*futurepositionhis_ignore)
        futurepositiondetailhis_result = base.compare_dict(futurepositiondetailhis_database, futurepositiondetailhis_excel,
                                                        'futurepositiondetail2022',*futurepositiondetailhis_ignore)
        # futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition')
        # futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
        #                                                 'futurepositiondetail',*futurepositiondetail_ignore)
        # 断言
        final_result = futuretradinglog_result  + futurepositionhis_result + futurepositiondetailhis_result\

        if not (final_result and futurepositiondetail_database and futureposition_database):
            logger().info('沪权\过期 对比数据无异常')
            assert True
        else:
            logger().error('沪权\过期 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
