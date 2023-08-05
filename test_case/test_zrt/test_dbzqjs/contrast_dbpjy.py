import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastDateOfPayment(unittest.TestCase):
    """
     转融通\担保证券结算\担保品买卖
    """
    yaml = BaseAction().read_yaml(path=PathConfig().zrt())['DBZQJS']['DBPJY']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_date_of_payment(self):
        """
         转融通\担保证券结算\担保品买卖
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行： 转融通\担保证券结算\担保品买卖 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where  stkid in('600016','000651','000002','000001','600000')" \
                      " and acctid ='555000000003'"
        tradinglog_sql = "select b.INTERIORDESC,a.* from tradinglog{} a ,briefdefine b where a.briefid=b.briefid  and" \
                         " a.reckoningtime>={} and a.reckoningtime<={} and  acctid ='555000000003' and a.briefid" \
                         " in('005_001_001','005_002_001')  ".format(year,begintime,endtime)
        RC_CMOStklist_sql = "select * from RC_CMOStklist where stkid in('600016','000651','000002','000001','600000') " \
                            "and offerregid in('D890023504','0689899889') "

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        RC_CMOStklist_database = base.rc_comsktlist_sort(oracle.dict_data(RC_CMOStklist_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        RC_CMOStklist_excel = base.rc_comsktlist_sort(excel.read_excel('RC_CMOStklist'))
        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        RC_CMOStklist_result = base.compare_dict(RC_CMOStklist_database,RC_CMOStklist_excel,'RC_CMOStklist')
        # 断言
        final_result = stklist_result + tradinglog_result + RC_CMOStklist_result
        if not final_result:
            logger().info(' 转融通\担保证券结算\担保品买卖 对比数据无异常')
            assert True
        else:
            logger().error(' 转融通\担保证券结算\担保品买卖 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
