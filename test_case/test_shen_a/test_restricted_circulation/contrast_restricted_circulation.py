import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedCirculation(unittest.TestCase):
    """
    深A/限售股转流通股
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['restrictedCirculation']

    def test_restricted_circulate(self):
        """
        深A/限售股转流通股
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 深A/限售股转流通股 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        stklist_sql = "select * from STKLIST{} where EXCHID = '1' and REGID ='0117212000' and STKID in " \
                      "('002324','109676','300412') and DESKID = '077011'".format(year)
        stklistextend_sql = "select * FROM stklistextend{}  where exchid='1' and stkid in " \
                            "('002324','109676','300412') and DESKID ='077011' and REGID ='0117212000'".format(year)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         " stkid in ('002324','109676','300412') and briefid in('005_004_043','005_003_002'," \
                         "'005_003_015','005_004_015')".format(year, begintime, endtime)
        exchangerights_sql = "select * FROM exchangerights  where exchid='1' and stkid in ('002324','109676','300412') " \
                             "and DESKID ='077011' and REGID = '0117212000'"
        # 查询数据库并排序
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        # 查询excel数据并排序
        stklist_excel = base.stklist_sort(excel.read_excel('stklist2022'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend2022'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2022'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        # 忽略字段
        stklist_ignore = ()
        stklistextend_ignore = ()
        tradinglog_ignore = ()
        exchangerights_ignore = ()
        # 对比结果
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextend_result = base.compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog')
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        # 断言
        final_result = stklist_result + stklistextend_result + tradinglog_result + exchangerights_result
        if not final_result:
            logger().info('深A/限售股转流通股 数据对比无异常')
            assert True
        else:
            logger().error('深A/限售股转流通股 数据对比异常:{}'.format(final_result))
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
