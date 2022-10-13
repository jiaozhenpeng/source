import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplitXL(unittest.TestCase):
    """
    沪A\ETF拆分\限售股分配
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['EtfSplit']['XL']

    def test_etf_split_xl(self):
        """
        沪A\ETF拆分\限售股分配
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\ETF拆分\限售股分配 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where exchid='0' and stkid in('511210','513030') and " \
                      "offerregid in('A117212000','A117252000')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid in('511210','513030') and briefid in('005_003_121')".format(year,begintime,endtime)
        stklistextend_sql = "select * from stklistextend where  exchid='0' AND exchid='0' " \
                            "and stkid in('511210','513030') and offerregid in('A117212000','A117252000')"
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        # 忽略字段
        stklist_ignore = ()
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
            'POSTAMT')
        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklistextend_result = base.compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')
        # 断言
        final_result =  stklist_result+ tradinglog_result   + stklistextend_result
        if not final_result:
            logger().info('沪A\ETF拆分\限售股分配 对比数据无异常')
            assert True
        else:
            logger().error('沪A\ETF拆分\限售股分配 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
