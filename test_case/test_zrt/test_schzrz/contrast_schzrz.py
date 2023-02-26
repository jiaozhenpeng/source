import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    转融通\市场化转融资
    """
    yaml = BaseAction().read_yaml(path=PathConfig().zrt())['SCHZRZ']['tday']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        转融通\市场化转融资
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：转融通\市场化转融资 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        rc_cashborrowlog_sql = " SELECT TO_CHAR(CONTRACTNO) CONTRACTNO,APPSHEETSERIALNO,ORIGCONTRACTNO,CONTRACTTYPE," \
                               "CONTRACTSTATUS,ACCTID,CURRENCYID,ACCTNAME,EXCHID,REGID,DESKID,TERM,BUYRATE,ORDERTIME," \
                               "CLOSEDATE,ROLLBACKDATE,CONTRACTAMT,INTEREST,OVERDRAFTINTEREST,FORFEIT,OTHERFEE," \
                               "DEPOSITSUM,EXTENDFLAG,MEMO,ISEXTENDCONTRACT,TARGETREGID,TARGETDESKID,APPOINTNO," \
                               "EXTENDSTATUS,EXTENDCFMAMT,EXTENDAUDITTIME,CONTRACTOWNER,EXTENDNUMINTRANSIT," \
                               "EXTENAMTINTRANSIT,GETACCOUNTDATE,GETACCOUNTNUM,EXECTYPE  FROM rc_cashborrowlog " \
                               "where appsheetserialno='0000025015'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0' and" \
                         "  contractnum ='0000025015' and briefid = '005_005_060'".format(year, begintime, endtime)

        # 数据库数据
        rc_cashborrowlog_database = base.rc_cashborrowlog_sort(oracle.dict_data(rc_cashborrowlog_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        # Excel数据
        rc_cashborrowlog_excel = base.rc_cashborrowlog_sort(excel.read_excel('rc_cashborrowlog'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        rc_cashborrowlog_ignore = self.ignore['rc_cashborrowlog']
        # 对比

        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        rc_cashborrowlog_result = base.compare_dict(rc_cashborrowlog_database,rc_cashborrowlog_excel
                                                    ,'rc_cashborrowlog',*rc_cashborrowlog_ignore)
        # 断言
        final_result =   tradinglog_result + rc_cashborrowlog_result
        if not (final_result ):
            logger().info('转融通\市场化转融资 对比数据无异常')
            assert True
        else:
            logger().error('转融通\市场化转融资 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
