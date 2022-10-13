import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastValueBasedPlacement(unittest.TestCase):
    """
    深A\发行业务\按值配售\T日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['IssuanceBusiness']['ValueBasedPlacement']

    def test_value_based_placement(self):
        """
        深A\发行业务\按值配售\T日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\发行业务\按值配售\T日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        newstkpurchaseinfo_sql = "select * from newstkpurchaseinfo where reckoningtime>={} and reckoningtime<={} and" \
                                 "  stkid in('300555','072004','002802') and regid = '0117605001' and " \
                                 "  exchid ='1'".format(begintime,endtime)
        # 数据库数据
        newstkpurchaseinfo_database = base.newstkpurchaseinfo_sort(oracle.dict_data(newstkpurchaseinfo_sql))
        # Excel数据
        newstkpurchaseinfo_excel = base.newstkpurchaseinfo_sort(excel.read_excel('newstkpurchaseinfo'))
        # 忽略字段
        newstkpurchaseinfo_ignore =('RECKONINGTIME','PATHDESKID','ALLOTDATE')
        openorder_ignore = ()
        # 对比
        newstkpurchaseinfo_result = base.compare_dict(newstkpurchaseinfo_database,newstkpurchaseinfo_excel,
                                                      'newstkpurchaseinfo',*newstkpurchaseinfo_ignore)
        # 断言
        final_result = newstkpurchaseinfo_result
        if not final_result:
            logger().info('深A\发行业务\按值配售\T日 对比数据无异常')
            assert True
        else:
            logger().error('深A\发行业务\按值配售\T日 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
