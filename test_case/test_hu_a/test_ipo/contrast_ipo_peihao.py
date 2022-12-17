import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\按值配售\T日（认购配号日）
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['IPO']['peihao']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪A\按值配售\T日（认购配号日）
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\按值配售\T日（认购配号日） 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        newstkpurchaseinfo_sql = "select * from newstkpurchaseinfo where reckoningtime>={} and exchid='0' and " \
                                 " ALLOTCODEFLAG='0' ".format(begintime,)

        # 数据库数据
        newstkpurchaseinfo_database = base.newstkpurchaseinfo_sort(oracle.dict_data(newstkpurchaseinfo_sql))

        # Excel数据
        newstkpurchaseinfo_excel = base.newstkpurchaseinfo_sort(excel.read_excel('newstkpurchaseinfo'))

        # 忽略字段
        newstkpurchaseinfo_ignore = self.ignore['newstkpurchaseinfo']
        # 对比

        newstkpurchaseinfo_result = base.compare_dict(newstkpurchaseinfo_database, newstkpurchaseinfo_excel,
                                                      'newstkpurchaseinfo', *newstkpurchaseinfo_ignore)
        # 断言
        final_result =  newstkpurchaseinfo_result
        if not final_result:
            logger().info('沪A\按值配售\T日（认购配号日） 对比数据无异常')
            assert True
        else:
            logger().error('沪A\按值配售\T日（认购配号日） 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
