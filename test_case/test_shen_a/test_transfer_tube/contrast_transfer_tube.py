import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastTransferTube(unittest.TestCase):
    """
    深A\深圳转托管
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['TransferTube']

    def test_transfer_tube(self):
        """
        深A\深圳转托管
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\深圳转托管 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where EXCHID = '1' and REGID in( '0117202000','0117202001','0117222000'," \
                      "'0117222001') and STKID in ('000952','002325') and DESKID = '077011'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         " stkid in ('000952','002325') and briefid in('005_004_001','003_002_003'," \
                         "'003_001_004')".format(year,begintime,endtime)
        stklist2022_sql = "select * from STKLIST{} where  occurtime={} and EXCHID = '1' and REGID in( '0117202000'," \
                          "'0117202001','0117222000','0117222001') and STKID in ('000952'," \
                          "'002325') and DESKID = '077011'".format(year,begintime)
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklist2022_database = base.stklist_sort(oracle.dict_data(stklist2022_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklist2022_excel = base.stklist_sort(excel.read_excel('stklist2022'))
        # 忽略字段
        stklist_ignore = ('OCCURTIME',)
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF','POSTAMT')
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklist2022_result = base.compare_dict(stklist2022_database,stklist2022_excel,'stklist2022',*stklist_ignore)
        # 断言
        final_result = stklist_result + tradinglog_result + stklist2022_result
        if not final_result:
            logger().info('深A\深圳转托管 对比数据无异常')
            assert True
        else:
            logger().error('深A\深圳转托管 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
