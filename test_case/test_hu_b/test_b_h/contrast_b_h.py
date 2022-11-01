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
        unprocessedreckoningresult_sql ="select * from unprocessedreckoningresult where EXCHID='2' and DESKID = 'hb001'" \
                                        " and STKID  ='900905' and REGID in ('0000888888','0000AB3522') "
        stklist_sql ="select * from STKLIST where EXCHID = '2' and REGID in('0000888888','0000AB3522') and " \
                     " STKID = '900905' and DESKID = 'hb001'"
        # 获取数据库数据并排序
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(
            oracle.dict_data(unprocessedreckoningresult_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        # 获取excel数据并排序
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(
            excel.read_excel('unprocessedreckoningresult'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        # 可以忽略的字段
        stkauditingerror_ignore = ('OCCURTIME', 'KNOCKTIME', 'BUSINESSDATE')
        unprocessedreckoningresult_ignore = ('KNOCKTIME','OFFERTIME')
        stklist_ignore = ()
        # 对比数据
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,
                                                                      unprocessedreckoningresult_excel,
                                                                      'unprocessedreckoningresult',
                                                                      *unprocessedreckoningresult_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        final_result =   unprocessedreckoningresult_result + stklist_result
        if not final_result:
            logger().info('沪B-b转h 对比数据无异常')
            assert True
        else:
            logger().error('沪B-b转h 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()