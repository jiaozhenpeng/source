import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\信用保护凭证\信用保护凭证质押入库
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['xybhpz']['pledge']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())


    def test_etf_split(self):
        """
        沪A\信用保护凭证\信用保护凭证质押入库
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\信用保护凭证\信用保护凭证质押入库 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where exchid='0' and stkid in('170023','170024') and " \
                      "offerregid in('A117212000','A117252000')"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid in ('170023','170024') ".format(year,begintime,endtime)
        stkauditingerror_sql = " select * from stkauditingerror where  exchid='0' and stkid in('170001','170002') and " \
                               "  businessdate={}".format(begintime,)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stkauditingerror_database = base.stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))

        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stkauditingerror_excel = base.stkauditingerror_sort(excel.read_excel('stkauditingerror'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        stkauditingerror_ignore = self.ignore['stkauditingerror']
        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stkauditingerror_result = base.compare_dict(stkauditingerror_database,stkauditingerror_excel,
                                           'stkauditingerror',*stkauditingerror_ignore)
        # 断言
        final_result =  stklist_result + tradinglog_result + stkauditingerror_result
        if not final_result:
            logger().info('沪A\信用保护凭证\信用保护凭证质押入库 对比数据无异常')
            assert True
        else:
            logger().error('沪A\信用保护凭证\信用保护凭证质押入库 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
