import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastOnSiteTrusteeship(unittest.TestCase):
    """
    沪A\基金通\场内转托管
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['FundsThrough']['OnSiteTrusteeship']

    def test_on_site_trusteeship(self):
        """
        沪A\基金通\场内转托管
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\基金通\场内转托管 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where EXCHID = '0' and REGID ='A117212000' and STKID in " \
                      "('508002','508000') and DESKID = '00W40'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0' " \
                         "and  stkid in ('508002','508000','508001') and briefid in('005_004_001'," \
                         "'005_003_001')".format(year,begintime,endtime)
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        # 忽略字段
        stklist_ignore = ()
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result = stklist_result + tradinglog_result
        if not final_result:
            logger().info('沪A\基金通\场内转托管 对比数据无异常')
            assert True
        else:
            logger().error('沪A\基金通\场内转托管 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()