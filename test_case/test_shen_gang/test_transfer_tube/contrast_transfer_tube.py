import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastTransferTube(unittest.TestCase):
    """
    深港\深港转托管
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_gang())['TransferTube']

    def test_transfer_tube(self):
        """
        深港\深港转托管
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深港\深港转托管 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql

        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '4'  " \
                         "and REGID in ('0117212001','0117252000','0117212000')  and  stkid in ('00004','00006'," \
                         "'00008','00011') and DESKID ='077011'".format(year,begintime, endtime)
        regrights_sql = "select * from regrights where EXCHID='4' and STKID in ('00004','00006','00008','00011') and " \
                        "REGID in ('0117212001','0117252000','0117212000')  and DESKID ='077011'"
        unprocessedreckoningresult_sql = "select * from unprocessedreckoningresult where EXCHID='4' and DESKID ='077011'" \
                                         " and STKID in ('00004') and REGID in ('0117212000') and ACCTID in " \
                                         "('000011721200') and knocktime>={}".format(begintime,)
        unprocessedreckoningresulthis_sql = "select * from unprocessedreckoningresulthis where EXCHID='4' and DESKID " \
                                            "= '077011' and STKID ='00004' and REGID ='0117212000' and ACCTID " \
                                            "='000011721200' and knocktime>={}".format(begintime,)
        stklisthis_sql = "select * from STKLIST{} where EXCHID = '4' and REGID in('0117212001','0117252000','0117212000') " \
                      "and STKID in ('00004','00006','00008','00011') and DESKID = '077011' and OCCURTIME = " \
                      "{}".format(year,begintime)
        stklist_sql = "select * from STKLIST where EXCHID = '4' and REGID in('0117212001','0117252000','0117212000') " \
                      "and STKID in ('00004','00006','00008','00011') and DESKID = '077011' ".format(year,begintime)
        # 数据库数据
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        regrights_database = base.regrights_sort(oracle.dict_data(regrights_sql))
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(
            oracle.dict_data(unprocessedreckoningresult_sql))
        unprocessedreckoningresulthis_database = base.unprocessedreckoningresulthis_sort(
            oracle.dict_data(unprocessedreckoningresulthis_sql))
        stklisthis_database = base.stklist_sort(oracle.dict_data(stklisthis_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        # Excel数据
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        regrights_excel = base.regrights_sort(excel.read_excel('regrights'))
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(
            excel.read_excel('unprocessedreckoningresult'))
        unprocessedreckoningresulthis_excel = base.unprocessedreckoningresulthis_sort(
            excel.read_excel('unprocessedreckoningresulthis'))
        stklisthis_excel = base.stklist_sort(excel.read_excel('stklist2021'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        # 忽略字段
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME',
                             'TRANSACTIONREF','SETTLEDATE','POSTAMT')
        regrights_ignore = ('OCCURTIME','POSTAMT')
        unprocessedreckoningresult_ignore = ('KNOCKTIME','TRANSACTIONREF','SETTLEDATE')
        unprocessedreckoningresulthis_ignore = ('KNOCKTIME','TRANSACTIONREF','SETTLEDATE')
        stklist_ignore = ('OCCURTIME',)
        # 对比
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        regrights_result = base.compare_dict(regrights_database, regrights_excel, 'regrights',*regrights_ignore)
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,
                                                              unprocessedreckoningresult_excel,
                                                              'unprocessedreckoningresult',
                                                              *unprocessedreckoningresult_ignore)
        unprocessedreckoningresulthis_result = base.compare_dict(unprocessedreckoningresulthis_database,
                                                                 unprocessedreckoningresulthis_excel,
                                                                 'unprocessedreckoningresulthis',
                                                                 *unprocessedreckoningresulthis_ignore)
        stklisthis_result = base.compare_dict(stklisthis_database, stklisthis_excel, 'stklist2022',*stklist_ignore)
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')


        # 断言
        final_result =  tradinglog_result + regrights_result + unprocessedreckoningresult_result \
                       + unprocessedreckoningresulthis_result + stklist_result + stklisthis_result
        if not final_result:
            logger().info('深港\深港转托管 对比数据无异常')
            assert True
        else:
            logger().error('深港\深港转托管 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()