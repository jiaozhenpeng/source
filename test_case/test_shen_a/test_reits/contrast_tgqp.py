import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastTransferTube(unittest.TestCase):
    """
    深A\公募reits\基金清盘(没分配虚拟股东，先保留错误)
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['Reits']['TGQP']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_transfer_tube(self):
        """
        深A\公募reits\基金清盘(没分配虚拟股东，先保留错误)
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\公募reits\基金清盘 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where EXCHID = '1'  and STKID in ('180003','180002','180005','180004') and DESKID = '077011'"
        tradinglog_sql = "select * from tradinglog{} where reckoningtime>={} and reckoningtime<={} and exchid= '1' and " \
                         " stkid in ('180003','180002','180005','180004') and briefid = '005_002_046' ".format(year,begintime,endtime)
        stklist2023_sql = "select * from STKLIST{} where  occurtime={} and EXCHID = '1' and STKID in" \
                          " ('180003','180002','180005','180004') and DESKID = '077011'".format(year,begintime)
        stklistextend2023_sql = "select * from STKLISTextend{} where  occurtime={} and EXCHID = '1' and STKID in" \
                          " ('180003','180002','180005','180004') and DESKID = '077011'".format(year,begintime)
        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stklist2023_database = base.stklist_sort(oracle.dict_data(stklist2023_sql))
        stklistextend2023_database = base.stklistextend_sort(oracle.dict_data(stklistextend2023_sql))
        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        stklist2023_excel = base.stklist_sort(excel.read_excel('stklist2023'))
        stklistextend2023_excel = base.stklistextend_sort(excel.read_excel('stklistextend2023'))

        # 忽略字段
        stklist_ignore = ('OCCURTIME',)
        tradinglog_ignore = self.ignore['tradinglog']
        stklistextend_ignore = self.ignore['stklistextendhis']
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = base.compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog', *tradinglog_ignore)
        stklist2023_result = base.compare_dict(stklist2023_database,stklist2023_excel,'stklist2023',*stklist_ignore)
        stklistextend2023_result = base.compare_dict(stklistextend2023_database,stklistextend2023_excel,
                                                     'stklistextend2023',*stklistextend_ignore)

        # 断言
        final_result = stklist_result + tradinglog_result + stklist2023_result + stklistextend2023_result
        if not final_result:
            logger().info('深A\公募reits\基金清盘 对比数据无异常')
            assert True
        else:
            logger().error('深A\公募reits\基金清盘 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
