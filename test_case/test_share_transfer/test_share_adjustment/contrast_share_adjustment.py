import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastShareAdjustment(unittest.TestCase):
    """
    对比 股转\股份调账
    """
    yaml = BaseAction().read_yaml(path=PathConfig().share_reconciliation())['ShareAdjustment']

    def test_adjustment(self):
        '''
        对比 股转\股份调账
        :return:
        '''
        logger().info('-------------------------')
        logger().info('开始对比  股转\股份调账 数据')
        oracle = OracleDatabase()
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        year = BaseAction().get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST where EXCHID = '6' and REGID in( 'GZ11721400','GZ11721600') and STKID in " \
                      "('839112','839111') and DESKID = 'ANQ001'"
        stklistextend_sql = "select * FROM stklistextend a where a.exchid='6' and a.stkid in ('839112','839111')   " \
                            "and a.acctid in ('000011721400','000011721600') and DESKID ='ANQ001' and REGID in" \
                            "( 'GZ11721400','GZ11721600')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '6' " \
                         " and briefid in('005_003_027','005_004_027') and stkid in" \
                         " ('839112','839111')".format(year, begintime, endtime)
        # 获取数据库数据并排序
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        stklistextend_database = BaseAction().stklistextend_sort(oracle.dict_data(stklistextend_sql))
        tradinglog_database = BaseAction().tradinglog_sort1(oracle.dict_data(tradinglog_sql))

        # 获取excel数据并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        stklistextend_excel = BaseAction().stklistextend_sort(excel.read_excel('stklistextend'))
        tradinglog_excel = BaseAction().tradinglog_sort1(excel.read_excel('tradinglog2021'))

        # 忽略字段
        stklist_ignore = ()
        stklistextend_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        # 对比数据
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextend_result = BaseAction().compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog',
                                                      *tradinglog_ignore)
        # 判断数据
        final_result = stklist_result + stklistextend_result + tradinglog_result
        if not final_result:
            logger().info('股转\股份调账 数据对比无异常')
            assert True
        else:
            logger().error('股转\股份调账 数据对比异常:{}'.format(final_result))
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
