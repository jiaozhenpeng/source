import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastReserveConversion(unittest.TestCase):
    """
    沪权\备兑转换
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['ReserveConversion']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_b_turn_h(self):
        """
        沪权\备兑转换
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\备兑转换 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        futuretradinglog_sql = "select * from futuretradinglog{}  where reckoningtime>={} and reckoningtime<={} and " \
                               "exchid='X' and regid='A117212005' and stkid in('10003956','10003959','10003982'," \
                               "'10003989')".format(year, begintime, endtime)
        futurepositionhis_sql = "select * from futureposition{} WHERE regid='A117212005'  and occurtime={} and stkid " \
                                "in('10003956','10003959','10003982','10003989')".format(year, begintime)
        futurepositiondetailhis_sql = "select * from futurepositiondetail{} WHERE regid='A117212005'  and occurtime={} " \
                                      "and stkid in('10003956','10003959','10003982','10003989')".format(year,
                                                                                                         begintime)

        futureposition_sql = "select * from futureposition WHERE regid='A117212005'   and stkid" \
                             " in('10003956','10003959','10003982','10003989') "
        futurepositiondetail_sql = "select * from futurepositiondetail WHERE regid='A117212005'   and stkid" \
                                   " in('10003956','10003959','10003982','10003989') "
        # 获取数据库数据
        futurepositiondetailhis_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetailhis_sql))
        futuretradinglog_database = base.futuretradinglog_sort(oracle.dict_data(futuretradinglog_sql))
        futurepositionhis_database = base.futureposition_sort(oracle.dict_data(futurepositionhis_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        # excel 数据
        futuretradinglog_excel = base.futuretradinglog_sort(excel.read_excel('futuretradinglog'))
        futurepositionhis_excel = base.futureposition_sort(excel.read_excel('futureposition2022'))
        futurepositiondetailhis_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail2022'))
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))

        # 忽略字段  合同号和成交编号自动生成，需忽略
        futuretradinglog_ignore = self.ignore['futuretradinglog1']
        futurepositionhis_ignore = self.ignore['futurepositionhis']
        futurepositiondetail_ignore = self.ignore['futurepositiondetail1']
        futurepositiondetailhis_ignore = self.ignore['futurepositiondetailhis1']

        # 对比结果
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog', *futuretradinglog_ignore)
        futurepositionhis_result = base.compare_dict(futurepositionhis_database, futurepositionhis_excel,
                                                     'futureposition2022', *futurepositionhis_ignore)
        futurepositiondetailhis_result = base.compare_dict(futurepositiondetailhis_database,
                                                           futurepositiondetailhis_excel,
                                                           'futurepositiondetail2022', *futurepositiondetailhis_ignore)
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition')
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail', *futurepositiondetail_ignore)
        # 断言
        final_result = futuretradinglog_result + futureposition_result + futurepositiondetail_result \
                       + futurepositionhis_result + futurepositiondetailhis_result
        if not final_result:
            logger().info('沪权\备兑转换 对比数据无异常')
            assert True
        else:
            logger().error('沪权\备兑转换 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
