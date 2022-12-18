import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    沪A\各种证券变动\00T
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['ChangesInSecurities']['T']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_restricted_shares(self):
        """
        沪A\各种证券变动\00T
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\各种证券变动\00T 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklistextend_sql = " select * from   stklistextend where exchid='0' and offerregid in('A117212000'," \
                            "'A117252000' ) and stkid in('603626','603629','603630','603863','603859','603860')"
        stklist_sql = "select * from  stklist where exchid='0' and offerregid in('A117212000','A117252000' ) " \
                      "and stkid in('603626','603629','603630','603863','603859','603860')"
        stklisthis_sql = " select * from stklist{} where occurtime={} and stkid in" \
                         " ('603626','603629','603630','603863','603859','603860') ".format(year,begintime)
        stklistextendhis_sql = " select * from stklistextend{} where occurtime={} and stkid in" \
                               " ('603626','603629','603630','603863','603859','603860') ".format(year,begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid in ('603626','603629','603630','603863','603859','603860') ".format(year, begintime, endtime)
        # 获取数据库数据并排序

        stklistextend_database = BaseAction().stklistextend_sort(oracle.dict_data(stklistextend_sql))
        stklistextendhis_database = BaseAction().stklistextend_sort(oracle.dict_data(stklistextendhis_sql))
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        stklisthis_database = BaseAction().stklist_sort(oracle.dict_data(stklisthis_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))



        # 获取excel数据并排序
        stklistextend_excel = BaseAction().stklistextend_sort(excel.read_excel('stklistextend'))
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklistextendhis_excel = BaseAction().stklistextend_sort(excel.read_excel('stklistextend2022'))
        stklisthis_excel = BaseAction().stklist_sort(excel.read_excel('stklist2022'))



        # 可以忽略的字段
        stklistextendhis_ignore= self.ignore['stklisthis']
        stklisthis_ignore = self.ignore['stklistextendhis']
        tradinglog_ignore = self.ignore['tradinglog']

        # 对比数据

        stklist_result = BaseAction().compare_dict(stklist_database,stklist_excel,'stklist')
        stklistextend_result = BaseAction().compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')
        stklisthis_result = BaseAction().compare_dict(stklisthis_database,stklisthis_excel,'stklist2022',*stklisthis_ignore)
        stklistextendhis_result = BaseAction().compare_dict(stklistextendhis_database,stklistextendhis_excel,
                                                            'stklistextend2022',*stklistextendhis_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)

        final_result = stklist_result + stklistextend_result + stklisthis_result + stklistextendhis_result + tradinglog_result

        # 断言
        if not final_result :
            logger().info('沪A\各种证券变动\00T 对比数据无异常')
            assert True
        else:
            logger().error('沪A\各种证券变动\00T 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()