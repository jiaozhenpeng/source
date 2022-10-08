import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastMakeOver(unittest.TestCase):
    """
    沪A\定向可转债\转让
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['MakeOver']

    def test_make_over(self):
        """
        沪A\定向可转债\转让
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\定向可转债\转让 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        exchangerights_sql = "select * FROM exchangerights  where exchid='0' and stkid in ('110809','110811')" \
                             "and DESKID ='00W40' and REGID ='A117212000'"
        stklist_sql = "select * from STKLIST where  EXCHID = '0' and REGID ='A117212000' " \
                      "and stkid in ('110809','110811') and DESKID = '00W40'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0' and" \
                         "  stkid in ('110809','110811') and briefid in ('005_001_001'," \
                         "'005_002_001')".format(year, begintime, endtime)
        todaytraderslt_sql = "select * from TODAYTRADERSLT where STKID in ('110809','110811') and DESKID = '00W40' " \
                             "and EXCHID = '0' and reckoningtime>={} and reckoningtime<={}".format(begintime,endtime)
        exchjsmxdetailinfo_sql = "select * from exchjsmxdetailinfo where reckoningtime>={} and reckoningtime<={} and" \
                                 " exchid= '0' and  stkid in ('110809','110811') and REGID = " \
                                 "'A117212000'".format(begintime,endtime)
        # 数据库数据
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        todaytraderslt_database = base.todaytraderslt_sort(oracle.dict_data(todaytraderslt_sql))
        exchjsmxdetailinfo_database =base.exchjsmxdetailinfo_sort(oracle.dict_data(exchjsmxdetailinfo_sql))
        # Excel数据
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2020'))
        todaytraderslt_excel = base.todaytraderslt_sort(excel.read_excel('todaytraderslt'))
        exchjsmxdetailinfo_excel = base.exchjsmxdetailinfo_sort(excel.read_excel('EXCHJSMXDETAILINFO'))
        # 忽略字段
        exchangerights_ignore = ()
        tradinglog_ignore = (
            'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        stklist_ignore = ()
        todaytraderslt_ignore = ('RECKONINGTIME', 'KNOCKTIME', 'SERIALNUM')
        exchjsmxdetailinfo_ignore = ()
        # 对比
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        todaytraderslt_result = base.compare_dict(todaytraderslt_database, todaytraderslt_excel, 'todaytraderslt',
                                                  *todaytraderslt_ignore)
        exchjsmxdetailinfo_result  = base.compare_dict(exchjsmxdetailinfo_database,exchjsmxdetailinfo_excel,
                                                       'exchjsmxdetailinfo')
        # 断言
        final_result = exchangerights_result + stklist_result + tradinglog_result + \
                       todaytraderslt_result + exchjsmxdetailinfo_result
        if not final_result:
            logger().info('沪A\定向可转债\转让 对比数据无异常')
            assert True
        else:
            logger().error(' 沪A\定向可转债\转让 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
