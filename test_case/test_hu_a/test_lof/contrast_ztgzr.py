import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    沪A\上证lof\lof跨市场转托管转入
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['lofztgzr']

    def test_restricted_shares(self):
        """
        沪A\上证lof\lof跨市场转托管转入
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\上证lof\lof跨市场转托管转入 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        tradinglog_sql = "select * from tradinglog{} where EXCHID='0' and STKID in ('501064','501065') and " \
                         "REGID in ('A117322000','A117322001') and reckoningtime>={} " \
                         "and reckoningtime<={}".format(year,begintime,endtime )
        stklist_sql = "select * from   stklist where regid in ('A117322000','A117322001') and stkid  in('501064','501065')"
        stklisthis_sql = "select * from   stklist{}  where occurtime={} and regid in ('A117322000','A117322001') and stkid " \
                         " in('501064','501065')".format(year,begintime)
        # 获取数据库数据并排序


        tradinglog_database = BaseAction().tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        stklisthis_database = BaseAction().stklist_sort(oracle.dict_data(stklisthis_sql))
        # 获取excel数据并排序

        tradinglog_excel = BaseAction().tradinglog_sort(excel.read_excel('tradinglog'))
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        stklisthis_excel = BaseAction().stklist_sort(excel.read_excel('stklist2022'))
        # 可以忽略的字段
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME',
                             'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        stklisthis_ignore = ('OCCURTIME',)
        # 对比数据

        tradinglog_result = BaseAction().compare_dict(tradinglog_database,tradinglog_excel,
                                                                      'tradinglog',*tradinglog_ignore)
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        stklisthis_result = BaseAction().compare_dict(stklisthis_database, stklisthis_excel, 'stklist2022',*stklisthis_ignore)


        final_result =   tradinglog_result + stklist_result + stklisthis_result

        # 断言
        if not final_result :
            logger().info('沪A\上证lof\lof跨市场转托管转入 对比数据无异常')
            assert True
        else:
            logger().error('沪A\上证lof\lof跨市场转托管转入 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()