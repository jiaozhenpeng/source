import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪银行\买卖交易\卖方银行间一级交收失败
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_bank())['ordinary_trade']['sell_yijifailed']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪银行\买卖交易\卖方银行间一级交收失败
        该记录失败，是因为还有问题，待优化，先这么失败着
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪银行\买卖交易\卖方银行间一级交收失败 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where exchid='C' and stkid in('092100008') "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= 'C'  " \
                         "and (stkid in ('092100008') or (reckoningamt=-150 and briefid='005_005_093' )) and ordertype='S' ".format(year, begintime, endtime)
        stklisthis_sql = "select * from STKLIST{} where exchid='C' and stkid in('092100008') " \
                         " and occurtime={}".format(year,begintime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort3(oracle.dict_data(tradinglog_sql))
        stklisthis_database = base.stklist_sort(oracle.dict_data(stklisthis_sql))


        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort3(excel.read_excel('tradinglog'))
        stklisthis_excel = base.stklist_sort(excel.read_excel('stklist2022'))


        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        stklisthis_ignore = self.ignore['stklisthis']

        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklisthis_result = base.compare_dict(stklisthis_database, stklisthis_excel, 'stklist2022',*stklisthis_ignore)

        # 断言
        final_result =   tradinglog_result + stklist_result + stklisthis_result
        if not final_result :
            logger().info('沪银行\买卖交易\卖方银行间一级交收失败 对比数据无异常')
            assert True
        else:
            logger().error('沪银行\买卖交易\卖方银行间一级交收失败 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
