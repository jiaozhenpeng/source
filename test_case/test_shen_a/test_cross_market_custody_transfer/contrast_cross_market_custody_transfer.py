import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastCrossMarketCustodyTransfer(unittest.TestCase):
    """
    深A\债券跨市场转托管
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['CrossMarketCustodyTransfer']

    def test_cross_market_custody_transfer(self):
        """
        深A\债券跨市场转托管
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\债券跨市场转托管 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST{} where OCCURTIME ={} and EXCHID = '1' and REGID in ('0117212000'," \
                      "'0117252000') and  stkid in('190185','190186') and DESKID = '077011'".format(year, begintime)
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and" \
                         "  stkid in('190185','190186') and briefid in ('005_003_002','003_002_003'," \
                         "'005_004_002')".format(year, begintime, endtime)
        stklistcurrent_sql = "select * from STKLIST where  EXCHID = '1' and REGID in ('0117212000'," \
                      "'0117252000') and  stkid in('190185','190186') and DESKID = '077011'"
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklistcurrent_database = base.stklist_sort(oracle.dict_data(stklistcurrent_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist2022'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2022'))
        stklistcurrent_excel = base.stklist_sort(excel.read_excel('stklist'))
        # 忽略字段
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        stklist_ignore = ('OCCURTIME',)
        # 对比
        stklistcurrent_result = base.compare_dict(stklistcurrent_database,stklistcurrent_excel, 'stklist')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist2022',*stklist_ignore)
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result =  stklistcurrent_result + stklist_result + tradinglog_result
        if not final_result:
            logger().info('深A\债券跨市场转托管 对比数据无异常')
            assert True
        else:
            logger().error('深A\债券跨市场转托管 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()


