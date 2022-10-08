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
        futureposition_sql = "select * from futureposition{} WHERE regid='A117212005'  and occurtime={} and stkid" \
                             " in('10003956','10003959','10003982','10003989') and exchid = 'x'".format(year, begintime)
        futurepositiondetail_sql = "select * from futurepositiondetail{} WHERE regid='A117212005'  and occurtime={} " \
                                   "and stkid in('10003956','10003959','10003982','10003989') and exchid = 'x'".format(
            year, begintime)
        stkoptionsettlement_sql = "select * from stkoptionsettlement{}  where reckoningtime>={} and reckoningtime<={}" \
                                  " and exchid='X' and regid='A117212005' and stkid in('10003956','10003959'," \
                                  "'10003982','10003989')".format(year, begintime, endtime)
        # 数据库数据
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        stkoptionsettlement_database = base.stkoptionsettlement_sort(oracle.dict_data(stkoptionsettlement_sql))
        # excel数据
        futureposition_excel = base.futureposition_sort(excel.read_excel('futureposition'))
        stkoptionsettlement_excel = base.stkoptionsettlement_sort(excel.read_excel('stkoptionsettlement'))
        futurepositiondetail_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail'))
        #  忽略字段
        futureposition_ignore = ('OCCURTIME',)
        futurepositiondetail_ignore = ()
        stkoptionsettlement_ignore = ()
        # 结果
        futureposition_result = base.compare_dict(futureposition_database, futureposition_excel, 'futureposition',
                                                  *(futureposition_ignore))
        futurepositiondetail_result = base.compare_dict(futurepositiondetail_database, futurepositiondetail_excel,
                                                        'futurepositiondetail')
        stkoptionsettlement_result = base.compare_dict(stkoptionsettlement_database, stkoptionsettlement_excel,
                                                       'stkoptionsettlement')

        final_result = futureposition_result + futurepositiondetail_result + stkoptionsettlement_result
        if not final_result:
            logger().info('沪权\备兑转换 对比数据无异常')
            assert True
        else:
            logger().error('沪权\备兑转换 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
