import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRepo(unittest.TestCase):
    """
    对比 深A\协议回购\T日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['repo']

    def test_repo(self):
        """
        对比 深A\协议回购\T日
        :return:
        """
        logger().info('-------------------------')
        logger().info('开始对比 深A\协议回购\T日 数据')
        excel_path = self.yaml['excelPath']
        oracle = OracleDatabase()
        excel = ExcelOperation(excel_path)
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         " stkid in ('109517','100213','109516') and briefid in('005_002_044','005_004_078','005_001_043')".format(
            year, begintime, endtime)
        stklist_sql = "select * from STKLIST where EXCHID = '1' and REGID in( '0117252001','0117212001') and STKID" \
                      " in ('109517','100213','109516','109644') and DESKID = '077011'"
        unduerepurchasebonds_sql = "select * from unduerepurchasebonds where EXCHID = '1' and REGID in( '0117252001'," \
                                   "'0117212001') and STKID in ('109517','100213','109516') and DESKID = '077011'"
        unduerepurchasebondshis_sql = "select * from unduerepurchasebondshis where EXCHID = '1' and REGID in( '0117252001'," \
                                      "'0117212001') and STKID in ('109517','100213','109516') and DESKID = '077011'"
        quoteRepoPledgeDtl_sql = "select * from quoteRepoPledgeDtl where REGID in ( '0117252001','0117212001') and " \
                                 "EXCHID = '1' and STKID in ('109517','100213','109516') "
        exchangerights_sql = "select * FROM exchangerights  where exchid='1' and stkid in ('109517','100213','109516') and" \
                             " DESKID ='077011' and REGID in ( '0117212000','0117252000','0117252001','0117212001')"
        exchangemessage_sql = "select * from exchangemessage where STKID in ('109517','100213','109516') and EXCHID = '1'"
        # 查询数据库SQL数据并排序
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        unduerepurchasebonds_database = base.unduerepurchasebonds_sort(oracle.dict_data(unduerepurchasebonds_sql))
        unduerepurchasebondshis_database = base.unduerepurchasebondshis_sort(
            oracle.dict_data(unduerepurchasebondshis_sql))
        quoteRepoPledgeDtl_database = base.quoteRepoPledgeDtl_sort(oracle.dict_data(quoteRepoPledgeDtl_sql))
        exchangerights_database = base.exchangerights_sort(oracle.dict_data(exchangerights_sql))
        exchangemessage_database = base.exchangemessage_sort(oracle.dict_data(exchangemessage_sql))
        # 查询excel数据并排序
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog2020'))
        unduerepurchasebonds_excel = base.unduerepurchasebonds_sort(excel.read_excel('unduerepurchasebonds'))
        unduerepurchasebondshis_excel = base.unduerepurchasebondshis_sort(excel.read_excel('unduerepurchasebondshis'))
        quoteRepoPledgeDtl_excel = base.quoteRepoPledgeDtl_sort(excel.read_excel('quoteRepoPledgeDtl'))
        exchangerights_excel = base.exchangerights_sort(excel.read_excel('exchangerights'))
        exchangemessage_excel = base.exchangemessage_sort(excel.read_excel('exchangemessage'))
        # 忽略字段
        stklist_ignore = ()
        tradinglog_ignore = ()
        unduerepurchasebonds_ignore = ()
        unduerepurchasebondshis_ignore = ()
        quoteRepoPledgeDtl_ignore = ()
        exchangerights_ignore = ()
        exchangemessage_ignore = ()
        # 对比结果
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog')
        unduerepurchasebonds_result = base.compare_dict(unduerepurchasebonds_database, unduerepurchasebonds_excel,
                                                        'unduerepurchasebonds')
        unduerepurchasebondshis_result = base.compare_dict(unduerepurchasebondshis_database,
                                                           unduerepurchasebondshis_excel, 'unduerepurchasebondshis')
        quoteRepoPledgeDtl_result = base.compare_dict(quoteRepoPledgeDtl_database, quoteRepoPledgeDtl_excel,
                                                      'quoteRepoPledgeDtl')
        exchangerights_result = base.compare_dict(exchangerights_database, exchangerights_excel, 'exchangerights')
        exchangemessage_result = base.compare_dict(exchangemessage_database, exchangemessage_excel, 'exchangemessage')
        # 断言
        final_result = stklist_result + tradinglog_result + unduerepurchasebonds_result + unduerepurchasebondshis_result\
                       + quoteRepoPledgeDtl_result + exchangerights_result + exchangemessage_result

        if not final_result:
            logger().info('深A\协议回购\T日 数据对比无异常')
            assert True
        else:
            logger().error('深A\协议回购\T日 数据对比异常:{}'.format(final_result))
            assert False, final_result

    if __name__ == '__main__':
        unittest.main()
