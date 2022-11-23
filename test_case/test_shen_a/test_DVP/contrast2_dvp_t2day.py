import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    深A\DVP改革\违约处置（T+2）
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['DVP']['Tday2']

    def test_restricted_shares(self):
        """
        深A\DVP改革\违约处置（T+2）
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\DVP改革\违约处置（T+2） 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklistextend_sql = " select * from  stklistextend where exchid='1' and offerregid in('0117212000'," \
                            "'0117252000') and  stkid in('000156','300014','108177','159996','123040','180012')"
        stklist_sql = "select * from    stklist where exchid='1' and offerregid in('0117212000','0117252000') " \
                      "and stkid in('000156','300014','108177','159996','123040','180012')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1'  " \
                         "and  briefid in('005_003_113','005_004_027') and regid in('0117212000','0117252000'" \
                         ",'0117212001' ,'0117252001') and" \
                         " stkid in('000156','300014','108177','159996','123040','180012') ".format(year, begintime, endtime)

        # 获取数据库数据并排序

        stklistextend_database = BaseAction().stklistextend_sort(oracle.dict_data(stklistextend_sql))
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # 获取excel数据并排序
        # stklistextend_excel = BaseAction().stklistextend_sort(excel.read_excel('stklistextend'))
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))

        # 可以忽略的字段
        stklistextend_ignore= ()
        stklist_ignore = ()
        tradinglog_ignore = ('KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME',
                             'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        # 对比数据

        stklist_result = BaseAction().compare_dict(stklist_database,stklist_excel,'stklist')
        # stklistextend_result = BaseAction().compare_dict(stklistextend_database,stklistextend_excel,'stklistextend')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)

        final_result = stklist_result  + tradinglog_result

        # 断言
        if not final_result :
            logger().info('深A\DVP改革\违约处置（T+2） 对比数据无异常')
            assert True
        else:
            logger().error('深A\DVP改革\违约处置（T+2） 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()