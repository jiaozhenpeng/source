import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastVirtualExer(unittest.TestCase):
    """
    转融通\权益合约\配股权益
    """
    yaml = BaseAction().read_yaml(path=PathConfig().zrt())['QYHY']['PGQY']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())


    def test_virtualexer(self):
        """
        转融通\权益合约\配股权益
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：转融通\权益合约\配股权益 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        shortbegintime = begintime[:8]
        # 查询SQL
        rc_sharelendlog_sql = "SELECT  TO_CHAR(CONTRACTNO) CONTRACTNO,CONTRACTNUM,KNOCKNUM,TO_CHAR(ORIGCONTRACTNO) ORIGCONTRACTNO,CONTRACTTYPE,CONTRACTSTATUS,ACCTID,CURRENCYID," \
                              "ACCTNAME,EXCHID,REGID,OFFERREGID,DESKID,STKID,TERM,SELLRATE,ORDERTIME," \
        "CLOSEDATE,ROLLBACKDATE,CONTRACTQTY,CLOSEPRICE,CONTRACTAMT,INTEREST,OVERDRAFTINTEREST,FORFEIT,OTHERFEE,EXTENDFLAG,RECOVERFLAG,RECOVERAUDITRSLT,MEMO,TARGETINFO,ISEXTENDCONTRACT," \
        "CASHREPLACEAMT,TARGETREGID,TARGETDESKID,APPOINTNO,EXTENDSTATUS,EXTENDCFMQTY,EXTENDAUDITTIME,EXTENDAPPOINTNO,EXTENDNUMINTRANSIT,EXTENAMTINTRANSIT,GETACCOUNTDATE,GETACCOUNTNUM," \
        "RECOVERSTATUS,RECOVERREASON,RECOVERCFMQTY,RECOVERCFMAMT,RECOVERAPPOINTNO,RECOVERAUDITTIME,COMMISSIONRATE,ACTUALCOMMISSION,EXPECTCOMMISSION,EXECTYPE,OTHERCODE,CONTRACT_ID," \
        "TO_CHAR(TARGETCONTRACTNO) TARGETCONTRACTNO,rightstype FROM RC_SHARELENDLOG where contractno in(2024082200002177, 2024082200002183, 2024082200002184, 2024082200002185," \
                              "  2024082200002186, 2024082200002187, 2024082200002190, 2024082200002191,2024082200002193,2024072300025903)  "

        rc_shareborrowlog_sql = " SELECT TO_CHAR(CONTRACTNO) CONTRACTNO,APPSHEETSERIALNO,TO_CHAR(ORIGCONTRACTNO) ORIGCONTRACTNO,CONTRACTTYPE,CONTRACTSTATUS,ACCTID,REGID,REGNAME" \
                                ",CURRENCYID,OFFERREGID,EXCHID,DESKID,STKID,TERM,BUYRATE,ADDRATE,ORDERTIME,CLOSEDATE,ROLLBACKDATE,CONTRACTQTY," \
                 "CLOSEPRICE,CONTRACTAMT,INTEREST,OVERDRAFTINTEREST,FORFEIT,OTHERFEE,DEPOSITSUM,EXTENDFLAG,RECOVERFLAG,MEMO,TARGETINFO,ISEXTENDCONTRACT,CASHREPLACEAMT," \
                 "TARGETREGID,TARGETDESKID,APPOINTNO,EXTENDSTATUS,EXTENDCFMQTY,EXTENDAUDITTIME,EXTENDAPPOINTNO,CONTRACTOWNER,EXTENDNUMINTRANSIT,EXTENAMTINTRANSIT,GETACCOUNTDATE," \
                 "GETACCOUNTNUM,RECOVERSTATUS,RECOVERREASON,RECOVERCFMQTY,RECOVERCFMAMT,RECOVERAPPOINTNO,RECOVERAUDITTIME,EXECTYPE,TO_CHAR(TARGETCONTRACTNO) TARGETCONTRACTNO,rightstype" \
                                " from Rc_Shareborrowlog  where contractno in(2024082200002177, 2024082200002183, 2024082200002184, 2024082200002185," \
                              "  2024082200002186, 2024082200002187, 2024082200002190, 2024082200002191,2024082200002193,2024072300028207)  "

        tradinglog_sql = "select b.INTERIORDESC,a.* from tradinglog{} a ,briefdefine b where a.briefid=b.briefid  and" \
                         " a.briefid in('005_004_056','005_003_058') and stkid='300893' and a.reckoningtime>={} and " \
                         "a.reckoningtime<={} ".format(year,begintime,endtime)

        rc_stkrights_sql = "select * from  rc_stkrights{} where reckoningtime>={} and reckoningtime<={} and  " \
                           "rightstype='6' ".format(year,begintime,endtime)

        # 获取数据库数据
        rc_sharelendlog_database = base.rc_sharelendlog_sort(oracle.dict_data(rc_sharelendlog_sql))
        rc_shareborrowlog_database = base.rc_shareborrowlog_sort(oracle.dict_data(rc_shareborrowlog_sql))
        tradinglog_database = base.tradinglog_sort5(oracle.dict_data(tradinglog_sql))
        rc_stkrights_database = base.rc_stkrights_sort(oracle.dict_data(rc_stkrights_sql))

        # excel 数据
        rc_sharelendlog_excel = base.rc_sharelendlog_sort(excel.read_excel('RC_SHARELENDLOG'))
        rc_shareborrowlog_excel = base.rc_shareborrowlog_sort(excel.read_excel('Rc_Shareborrowlog'))
        tradinglog_excel = base.tradinglog_sort5(excel.read_excel('tradinglog'))
        rc_stkrights_excel = base.rc_stkrights_sort(excel.read_excel('RC_STKRIGHTS'))
        # 忽略字段
        rc_stkrights_ignore = self.ignore['RC_STKRIGHTS']
        rc_sharelendlog_ignore = self.ignore['rc_sharelendlog']
        rc_shareborrowlog_ignore = self.ignore['rc_shareborrowlog']
        tradinglog_ignore = self.ignore['tradinglog']

        # 对比结果
        rc_sharelendlog_result = base.compare_dict(rc_sharelendlog_database, rc_sharelendlog_excel,'rc_sharelendlog',*rc_sharelendlog_ignore)
        rc_shareborrowlog_result = base.compare_dict(rc_shareborrowlog_database, rc_shareborrowlog_excel,'rc_shareborrowlog',*rc_shareborrowlog_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
        rc_LendDer_result = base.compare_dict(rc_stkrights_database,rc_stkrights_excel,'rc_stkrights',*rc_stkrights_ignore)
        # 断言
        final_result =   rc_LendDer_result + rc_sharelendlog_result + rc_shareborrowlog_result + tradinglog_result

        if not final_result:
            logger().info('转融通\权益合约\配股权益 对比数据无异常')
            assert True
        else:
            logger().error('转融通\权益合约\配股权益 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()