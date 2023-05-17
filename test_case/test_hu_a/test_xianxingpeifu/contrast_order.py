import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\先行赔付\赔付申报
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['xianxingpeifu']['order']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪A\先行赔付\赔付申报
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\先行赔付\赔付申报 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        newstkpurchaseinfo_sql = "select * from newstkpurchaseinfo where reckoningtime>={} and exchid='0' and " \
                                 " ALLOTCODEFLAG='4' and stkid='688086' ".format(begintime, )

        # 数据库数据
        newstkpurchaseinfo_database = base.newstkpurchaseinfo_sort1(oracle.dict_data(newstkpurchaseinfo_sql))

        # Excel数据
        newstkpurchaseinfo_excel = base.newstkpurchaseinfo_sort1(excel.read_excel('newstkpurchaseinfo'))

        # 忽略字段
        newstkpurchaseinfo_ignore = self.ignore['newstkpurchaseinfo']
        # 对比

        newstkpurchaseinfo_result = base.compare_dict(newstkpurchaseinfo_database, newstkpurchaseinfo_excel,
                                                      'newstkpurchaseinfo', *newstkpurchaseinfo_ignore)
        # 断言
        final_result =  newstkpurchaseinfo_result
        if not final_result:
            logger().info('沪A\先行赔付\赔付申报 对比数据无异常')
            assert True
        else:
            logger().error('沪A\先行赔付\赔付申报 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
