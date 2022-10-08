import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation

class ContrastBH(unittest.TestCase):
    """
    沪B-b转h
    """
    yaml =  BaseAction().read_yaml(path=PathConfig().hu_b())['BH']
    def test_b_turn_h(self):
        """
        沪B-b转h
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪B-b转h 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        # 查询SQL
        # todaytraderslt_sql ="select * from TODAYTRADERSLT where STKID ='900905' and DESKID = 'hb001' and EXCHID = '2' " \
        #                     "and reckoningtime>={} and reckoningtime<={}".format(begintime,endtime)
        # finalreckoningresult_sql = "select * from finalreckoningresult where EXCHID='2' and DESKID = 'hb001' and " \
        #                            " STKID ='900905' and REGID in ('0000888888','0000AB3522') "
        unprocessedreckoningresult_sql ="select * from unprocessedreckoningresult where EXCHID='2' and DESKID = 'hb001'" \
                                        " and STKID  ='900905' and REGID in ('0000888888','0000AB3522') "
        stklist_sql ="select * from STKLIST where EXCHID = '2' and REGID in('0000888888','0000AB3522') and " \
                     " STKID = '900905' and DESKID = 'hb001'"
        stkauditingerror_sql = " select * from stkauditingerror where exchid='2' and businessdate={} and " \
                               "offerregid ='0000888888' and stkid = '900905' ".format(begintime)
        # 获取数据库数据并排序
        # todaytraderslt_database = base.todaytraderslt_sort(oracle.dict_data(todaytraderslt_sql))
        # finalreckoningresult_database = base.finalreckoningresult_sort(
        #     oracle.dict_data(finalreckoningresult_sql))
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(
            oracle.dict_data(unprocessedreckoningresult_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stkauditingerror_database = base.stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))
        # 获取excel数据并排序
        # todaytraderslt_excel = base.todaytraderslt_sort(excel.read_excel('todaytraderslt'))
        # finalreckoningresult_excel = base.finalreckoningresult_sort(excel.read_excel('finalreckoningresult'))
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(
            excel.read_excel('unprocessedreckoningresult'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stkauditingerror_excel = base.stkauditingerror_sort(excel.read_excel('stkauditingerror'))
        # 可以忽略的字段
        # todaytraderslt_ignore = ('RECKONINGTIME', 'KNOCKTIME', 'SERIALNUM')
        # finalreckoningresult_ignore = ('KNOCKTIME',)
        stkauditingerror_ignore = ('OCCURTIME', 'KNOCKTIME', 'BUSINESSDATE')
        unprocessedreckoningresult_ignore = ('KNOCKTIME',)
        stklist_ignore = ()
        # 对比数据
        # todaytraderslt_result = base.compare_dict(todaytraderslt_database, todaytraderslt_excel,
        #                                                   'todaytraderslt', *todaytraderslt_ignore)
        # finalreckoningresult_result = base.compare_dict(finalreckoningresult_database,
        #                                                         finalreckoningresult_excel, 'finalreckoningresult',
        #                                                         *finalreckoningresult_ignore)
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,
                                                                      unprocessedreckoningresult_excel,
                                                                      'unprocessedreckoningresult',
                                                                      *unprocessedreckoningresult_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stkauditingerror_result = base.compare_dict(stkauditingerror_database, stkauditingerror_excel,
                                                    'stkauditingerror', *stkauditingerror_ignore)
        final_result =  stkauditingerror_result + unprocessedreckoningresult_result + stklist_result
        if not final_result:
            logger().info('沪B-b转h 对比数据无异常')
            assert True
        else:
            logger().error('沪B-b转h 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()