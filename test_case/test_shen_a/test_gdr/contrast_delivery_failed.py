import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastDeliveryFailed(unittest.TestCase):
    """
    深A\GDR数据\交收失败
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['GDR']['DeliveryFailed']

    def test_delivery_failed(self):
        """
        深A\GDR数据\交收失败
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\GDR数据\交收失败 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        account_sql = "select * from ACCOUNT where ACCTID in ('000011721200','000011721201','000011725200'," \
                      "'000011725201')and CURRENCYID='00'"
        stklist_sql = "select * from STKLIST where EXCHID = '1' and REGID in( '0117212000','0117252000') and STKID" \
                      " ='002770' and DESKID = '077011'"
        exchangerights_sql = "select * FROM exchangerights  where exchid='1' and stkid='002770' and DESKID = '077011'" \
                             " and REGID in ('0117212000','0117252000','0117212001','0117252001')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1'  " \
                         "and REGID in ('0117212000','0117252000','0117212001','0117252001') and  stkid ='002770' and" \
                         " DESKID = '077011' and BRIEFID = '005_006_005'".format(year, begintime, endtime)
        virtualregistrationrights_sql = "select * from virtualregistrationrights where EXCHID='1' and REGID in " \
                                        "('0117212000','0117252000','0117212001','0117252001') and ORDERTYPE ='FJ01'"
        # 数据库数据
        account_database = base.account_sort(oracle.dict_data(account_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        virtualregistrationrights_database = base.virtualregistrationrights_sort(
            oracle.dict_data(virtualregistrationrights_sql))
        # Excel数据
        account_excel = base.account_sort(excel.read_excel('account'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        virtualregistrationrights_excel = base.virtualregistrationrights_sort(
            excel.read_excel('virtualRegistrationRights'))
        # 忽略字段
        account_ignore = ()
        stklist_ignore = ()
        exchangerights_ignore = ()
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE')
        virtualregistrationrights_ignore = ()
        # 对比
        account_result = base.compare_dict(account_database, account_excel, 'account')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        virtualregistrationrights_result = base.compare_dict(virtualregistrationrights_database,
                                                             virtualregistrationrights_excel,
                                                             'virtualregistrationrights')

        # 断言
        final_result = account_result + stklist_result + exchangerights_result + tradinglog_result + virtualregistrationrights_result
        if not final_result:
            logger().info('深A\GDR数据\交收失败 对比数据无异常')
            assert True
        else:
            logger().error('深A\GDR数据\交收失败 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()