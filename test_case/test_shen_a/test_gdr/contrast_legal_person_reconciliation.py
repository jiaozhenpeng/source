import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastLegalPersonReconciliation(unittest.TestCase):
    """
     深A\GDR数据\法人对账
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['GDR']['LegalPersonReconciliation']

    def test_legal_person_reconciliation(self):
        """
        深A\GDR数据\法人对账
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行： 深A\GDR数据\法人对账 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' " \
                         " and REGID in ('0117212001','0117252000','0117252001') and  stkid = '002770' and" \
                         " DESKID ='077011' and BRIEFID in ('005_003_093','005_005_076')".format(year, begintime, endtime)
        cf_reckdata_sql = "select * from cf_reckdata where DESKID='077011' and EXCHID='1' and STKID = '002770'"
        cf_recksum_sql = "select * from CF_RECKSUM where EXCHID='1' and DESKID='077011'"
        cf_reckdetail_sql = "select * from CF_RECKDETAIL where DESKID='077011' and EXCHID='1' and STKID = '002770'"
        cf_reckauditing_sql = "select * from CF_RECKAUDITING where EXCHID='1' "
        # 数据库数据
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        cf_reckdata_database = base.cf_reckdata_sort(oracle.dict_data(cf_reckdata_sql))
        cf_recksum_database = base.cf_recksum_sort(oracle.dict_data(cf_recksum_sql))
        cf_reckdetail_database = base.cf_reckdetail_sort(oracle.dict_data(cf_reckdetail_sql))
        cf_reckauditing_database = base.cf_reckauditing_sort(oracle.dict_data(cf_reckauditing_sql))
        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        cf_reckdata_excel = base.cf_reckdata_sort(excel.read_excel('CF_RECKDATA'))
        cf_recksum_excel = base.cf_recksum_sort(excel.read_excel('CF_RECKSUM'))
        cf_reckdetail_excel = base.cf_reckdetail_sort(excel.read_excel('CF_RECKDETAIL'))
        cf_reckauditing_excel = base.cf_reckauditing_sort(excel.read_excel('CF_RECKAUDITING'))
        # 忽略字段
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE')
        cf_reckdata_ignore = ()
        cf_recksum_ignore = ()
        cf_reckdetail_ignore = ()
        cf_reckauditing_ignore = ()
        # 对比
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        cf_reckdata_result = base.compare_dict(cf_reckdata_database, cf_reckdata_excel, 'CF_RECKDATA')
        cf_recksum_result = base.compare_dict(cf_recksum_database, cf_recksum_excel, 'CF_RECKSUM')
        cf_reckdetail_result = base.compare_dict(cf_reckdetail_database, cf_reckdetail_excel, 'CF_RECKDETAIL')
        cf_reckauditing_result = base.compare_dict(cf_reckauditing_database, cf_reckauditing_excel, 'CF_RECKAUDITING')
        # 断言
        final_result = tradinglog_result + cf_reckdata_result + cf_recksum_result + cf_reckdetail_result + cf_reckauditing_result
        if not final_result:
            logger().info(' 深A\GDR数据\法人对账 对比数据无异常')
            assert True
        else:
            logger().error(' 深A\GDR数据\法人对账 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()