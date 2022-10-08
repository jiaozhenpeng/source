import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfIssue(unittest.TestCase):
    """
    沪A\上海ETF发行\T+1日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['EtfIssue']['T1']

    def test_etf_issue(self):
        """
        沪A\上海ETF发行\T+1日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\上海ETF发行\T+1日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        todaytraderslt_sql = "select * from TODAYTRADERSLT where STKID in ('510334','510333','510330') and DESKID " \
                             "= '00W40' and EXCHID = '0' and reckoningtime>={} and reckoningtime<={}".format(begintime,endtime)
        finalreckoningresult_sql = "select * from finalreckoningresult where EXCHID='0' and DESKID = '00W40' and " \
                                   "STKID in ('510334','510333','510330') and REGID in ('A117605001') "
        exchjsmxdetailinfo_sql = "select * from exchjsmxdetailinfo where reckoningtime>={} and reckoningtime<={} and" \
                                 " exchid= '0' and  stkid in ('510334','510333','510330') and REGID in ('A117605000')" \
                                 "".format(begintime,endtime)
        stklist_sql = "select * from STKLIST where EXCHID = '0' and stkid in ('510334','510333','510330') and REGID" \
                      " in ('A117605001') and DESKID = '00W40'"
        stklistextend_sql = "select * FROM stklistextend  where exchid='0' and stkid in ('510334','510333','510330') " \
                            "and REGID in ('A117605001') and DESKID = '00W40'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and stkid in ('510334','510333','510330') and REGID in ('A117605001') and briefid " \
                         "in('005_001_006','005_002_006')".format(year,begintime,endtime)
        newstkpurchaseinfo_sql = "select * from newstkpurchaseinfo where reckoningtime>={} and reckoningtime<={} and " \
                                 "STKID in ('510334','510333','510330') and REGID in ('A117605001') and exchid =" \
                                 "'0'".format(year,begintime,endtime)
        # 数据库数据
        todaytraderslt_database = base.todaytraderslt_sort(oracle.dict_data(todaytraderslt_sql))
        finalreckoningresult_database = base.finalreckoningresult_sort(oracle.dict_data(finalreckoningresult_sql))
        exchjsmxdetailinfo_database = base.exchjsmxdetailinfo_sort(oracle.dict_data(exchjsmxdetailinfo_sql))
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        newstkpurchaseinfo_database = base.newstkpurchaseinfo_sort(oracle.dict_data(newstkpurchaseinfo_sql))
        # Excel数据
        todaytraderslt_excel = base.todaytraderslt_sort(excel.read_excel('todaytraderslt'))
        finalreckoningresult_excel = base.finalreckoningresult_sort(excel.read_excel('finalreckoningresult'))
        exchjsmxdetailinfo_excel = base.exchjsmxdetailinfo_sort(excel.read_excel('exchjsmxdetailinfo'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2021'))
        newstkpurchaseinfo_excel = base.newstkpurchaseinfo_sort(excel.read_excel('newstkpurchaseinfo'))
        # 忽略字段
        todaytraderslt_ignore = ('RECKONINGTIME', 'KNOCKTIME', 'SERIALNUM')
        finalreckoningresult_ignore = ('KNOCKTIME',)
        exchjsmxdetailinfo_ignore = ()
        stklist_ignore = ()
        stklistextend_ignore = ()
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        newstkpurchaseinfo_ignore = ('RECKONINGTIME',)
        # 对比
        todaytraderslt_result = base.compare_dict(todaytraderslt_database, todaytraderslt_excel, 'todaytraderslt',
                                                  *todaytraderslt_ignore)
        finalreckoningresult_result = base.compare_dict(finalreckoningresult_database,
                                                        finalreckoningresult_excel, 'finalreckoningresult',
                                                        *finalreckoningresult_ignore)
        exchjsmxdetailinfo_result = base.compare_dict(exchjsmxdetailinfo_database, exchjsmxdetailinfo_excel,
                                                      'exchjsmxdetailinfo')
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklistextend_result = base.compare_dict(stklistextend_database, stklistextend_excel, 'stklistextend')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        newstkpurchaseinfo_result = base.compare_dict(newstkpurchaseinfo_database, newstkpurchaseinfo_excel,
                                                      'newstkpurchaseinfo', *newstkpurchaseinfo_ignore)
        # 断言
        final_result = todaytraderslt_result + finalreckoningresult_result + exchjsmxdetailinfo_result + stklist_result\
                       + stklistextend_result + tradinglog_result + newstkpurchaseinfo_result
        if not final_result:
            logger().info('沪A\上海ETF发行\T+1日 对比数据无异常')
            assert True
        else:
            logger().error('沪A\上海ETF发行\T+1日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
