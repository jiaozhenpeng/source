import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation

''' 准备数据执行的sql与查询不一致，需确定
class ContrastB(unittest.TestCase):
    """
    沪A\\各种证券变动\\00B
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['ChangesInSecurities']['B']

    def test_00b(self):
        """
        沪A\\各种证券变动\\00B
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\\各种证券变动\\00B 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        exchangerights_sql = "select * FROM exchangerights  where exchid='0' and stkid in ('600000','600030')" \
                             "and DESKID ='00W40' and REGID in ('A117203000','A117212000')"
        stklist_sql = "select * from STKLIST where  EXCHID = '0' and REGID in ('A117203000','A117212000')" \
                      "and stkid in ('600000','600030') and DESKID = '00W40'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0' and" \
                         "  stkid in ('110813','110812','600988', '603788') and briefid in ('005_004_025'," \
                         "'005_003_025')".format(year, begintime, endtime)
        stklistextend_sql = "select * FROM stklistextend  where exchid='0' and stkid in ('600000','600030')" \
                            " and DESKID ='00W40' and REGID in ('A117203000','A117212000')"
        # 数据库数据
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        # Excel数据
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        # 忽略字段
        exchangerights_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME')
        stklist_ignore = ()
        stklistextend_ignore = ()
        # 对比
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklistextend_result = base.compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        # 断言
        final_result = exchangerights_result + stklist_result + tradinglog_result + stklistextend_result
        if not final_result:
            logger().info('沪A\\各种证券变动\\00B 对比数据无异常')
            assert True
        else:
            logger().error('沪A\\各种证券变动\\00B 对比数据异常')
            assert False, final_result

'''
if __name__ == '__main__':
    unittest.main()
