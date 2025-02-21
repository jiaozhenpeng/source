import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\融资融券\还券划拨
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['CreditTrade']['CreditHQHB']

    def test_etf_split(self):
        """
        沪A\融资融券\还券划拨
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\融资融券\还券划拨 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where exchid='0' and stkid in('600023') and " \
                      "ACCTID in('000000003469','777000000003')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid in ('600023') and " \
                         "briefid in('002_005_015','002_006_015','005_003_035','005_004_035','005_005_032','005_005_035')".format(year,begintime,endtime)
        creditshareloghis_sql = " select * from   creditshareloghis where occurtime={} and  acctid='000000003469' " \
                                " and stkid='600023' and creditshareid='732' ".format(begintime,)
        creditsharereturnlog_sql = " select * from  creditsharereturnlog where occurtime>={} and occurtime<={}" \
                                   " and exchid='0' and contractnum='0000000038' ".format(begintime,endtime)
        # 数据库数据并排序
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        creditshareloghis_database = base.creditshareloghis_sort(oracle.dict_data(creditshareloghis_sql))
        creditsharereturnlog_database = base.creditsharereturnlog_sort(oracle.dict_data(creditsharereturnlog_sql))


        # 取Excel数据并排序
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        creditshareloghis_excel = base.creditshareloghis_sort(excel.read_excel('creditshareloghis'))
        creditsharereturnlog_excel = base.creditsharereturnlog_sort(excel.read_excel('creditsharereturnlog'))
        # 忽略字段
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF',
            'POSTAMT')
        creditshareloghis_ignore = ('OCCURTIME','TRANSACTIONREF')
        creditsharereturnlog_ignore = ('OCCURTIME', )
        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        creditshareloghis_result = base.compare_dict(creditshareloghis_database, creditshareloghis_excel, 'creditshareloghis', *creditshareloghis_ignore)
        creditsharereturnlog_result = base.compare_dict(creditsharereturnlog_database, creditsharereturnlog_excel, 'creditsharereturnlog', *creditsharereturnlog_ignore)

        # 断言
        final_result =  stklist_result+ tradinglog_result + creditshareloghis_result + creditsharereturnlog_result
        if not final_result:
            logger().info('沪A\融资融券\还券划拨 对比数据无异常')
            assert True
        else:
            logger().error('沪A\融资融券\还券划拨 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
