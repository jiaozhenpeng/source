import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    F:\source\用例数据\深A\信用保护合约\CSSX实物结算
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['XYBHHY']['CSSX']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_restricted_shares(self):
        """
        F:\source\用例数据\深A\信用保护合约\CSSX实物结算
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：F:\source\用例数据\深A\信用保护合约\CSSX实物结算 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid='1' and " \
                         "briefid in('005_003_098','005_004_098')".format(year,begintime,endtime)
        stklist_sql = " select * from    stklist where exchid='1' and  regid IN ('0117212000','0117252000') " \
                      "  AND stkid IN ('112280','109674') "
        stklistextend_sql = "select * from    stklistextend where exchid='1' and  regid IN ('0117212000','0117252000') " \
                            "  AND stkid IN ('112280','109674')"

        # 获取数据库数据并排序

        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        # 获取excel数据并排序
        tradinglog_excel =  base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklist_excel =  base.stklist_sort(excel.read_excel('stklist'))
        stklistextend_excel =  base.stklistextend_sort(excel.read_excel('stklistextend'))
        # 可以忽略的字段
        tradinglog_ignore= self.ignore['tradinglog']
        # 对比数据

        tradinglog_result = BaseAction().compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
        stklist_result = BaseAction().compare_dict(stklist_database,stklist_excel,'stklist')
        stklistextend_result = BaseAction().compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')

        final_result = stklist_result + stklistextend_result + tradinglog_result

        # 断言
        if not final_result :
            logger().info('F:\source\用例数据\深A\信用保护合约\CSSX实物结算 对比数据无异常')
            assert True
        else:
            logger().error('F:\source\用例数据\深A\信用保护合约\CSSX实物结算 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()