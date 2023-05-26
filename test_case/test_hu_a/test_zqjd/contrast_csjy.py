import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\债券借贷\初始交易
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['zhaiquanjiedai']['csjy']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪A\先行赔付\权益登记日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\先行赔付\权益登记日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from stklist where exchid='0' and stkid in('018010','018011','508020'," \
                      "'508021','152002','152003','508027','508028','018016','018017') "
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '0'  " \
                         "and  briefid in ('005_003_110','005_004_015','005_004_111','005_004_112') and stkid in" \
                         "('018010','018011','508020','508021','508027','508028','018016','018017','152002','152003') ".format(year, begintime, endtime)
        unduerepurchasebonds_sql = "select * from unduerepurchasebonds where EXCHID = '0' and contracttype='JDHY' and" \
                                   " ordertime>={}".format(begintime,)
        unduerepurchasebondshis_sql = "select * from unduerepurchasebondshis where EXCHID = '0' and contracttype='JDHY' and" \
                                   " ordertime>={}".format(begintime,)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))

        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']
        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        # 断言
        final_result =  stklist_result + tradinglog_result
        if not final_result:
            logger().info('沪A\先行赔付\权益登记日 对比数据无异常')
            assert True
        else:
            logger().error('沪A\先行赔付\权益登记日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
