import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    股转 要约收购-预受要约
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['buyassumpsit']['ysyy']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        股转 要约收购-预受要约
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转 要约收购-预受要约 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from stklist where exchid='6' and offerregid='GZ11721600' and  stkid in('430033','430074','430002') "

        stklistextend_sql = "select * from stklistextend where exchid='6' and offerregid='GZ11721600' and  stkid in('430033','430074','430002')"

        unprocessedreckoningresult_sql = "select * FROM unprocessedreckoningresult where knocktime = {} and exchid='6'" \
                                         " and briefid in('005_004_023') and stkid in('430033','430074','430002')".format(begintime,)

        unprocessedreckoningresulthis_sql = "select * FROM unprocessedreckoningresulthis where knocktime = {} and exchid='6'" \
                                         " and briefid in('005_004_023') and stkid in('430033','430074','430002')".format(begintime,)
        


        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(oracle.dict_data(unprocessedreckoningresult_sql))
        unprocessedreckoningresulthis_database = base.unprocessedreckoningresulthis_sort(oracle.dict_data(unprocessedreckoningresulthis_sql))

        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(excel.read_excel('unprocessedreckoningresult'))
        unprocessedreckoningresulthis_excel = base.unprocessedreckoningresulthis_sort(excel.read_excel('unprocessedreckoningresulthis'))
        # 忽略字段
        unprocessedreckoningresult_ignore = self.ignore['unprocessedreckoningresult']
        unprocessedreckoningresulthis_ignore = self.ignore['unprocessedreckoningresulthis']



        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextend_result = base.compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,unprocessedreckoningresult_excel,
                                                              'unprocessedreckoningresult',*unprocessedreckoningresult_ignore)
        unprocessedreckoningresulthis_reuslt = base.compare_dict(unprocessedreckoningresulthis_database,
                                                                 unprocessedreckoningresulthis_excel,
                                                                 'unprocessedreckoningresulthis',*unprocessedreckoningresulthis_ignore)

        # 断言
        final_result =   stklist_result + stklistextend_result + unprocessedreckoningresult_result + unprocessedreckoningresulthis_reuslt
        if not final_result :
            logger().info('股转 要约收购-预受要约 对比数据无异常')
            assert True
        else:
            logger().error('股转 要约收购-预受要约 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
