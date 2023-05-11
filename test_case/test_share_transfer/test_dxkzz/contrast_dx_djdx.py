import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    股转\定向可转债\兑息\冻结兑息
    """
    yaml = BaseAction().read_yaml(path=PathConfig().share_reconciliation())['dxkzz']['djdx']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        股转\定向可转债\兑息\冻结兑息
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转\定向可转债\兑息\冻结兑息 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stklist_sql = "select * from STKLIST where exchid='9' and stkid in('810022') and " \
                      "offerregid in('GZ11721600')"
        custchglog_sql = "select * from custchglog{} where changetime>={} and changetime<={} and exchid= '9'  " \
                         "and stkid in ('810022') ".format(year,begintime,endtime)
        stklisthis_sql = "select * from STKLIST{} where occurtime={}  and exchid= '9'  " \
                         "and stkid in ('810022') and offerregid in('GZ11721600')".format(year,begintime)
        stklistextendhis_sql = "select * from stklistextend{} where  occurtime={} and exchid='9' and " \
                           "stkid='810022'".format(year,begintime)

        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        custchglog_database = base.custchglog_sort(oracle.dict_data(custchglog_sql))
        stklisthis_database = base.stklist_sort(oracle.dict_data(stklisthis_sql))
        stklistextendhis_database = base.stklistextend_sort(oracle.dict_data(stklistextendhis_sql))


        # Excel数据
        stklisthis_excel = base.stklist_sort(excel.read_excel('stklist2023'))
        custchglog_excel = base.custchglog_sort(excel.read_excel('custchglog2023'))
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklistextendhis_excel = base.stklistextend_sort(excel.read_excel('stklistextend2023'))

        # 忽略字段
        custchglog_ignore = self.ignore['custchglog']
        stklisthis_ignore =('OCCURTIME',)
        stklistextendhis_ignore = ('OCCURTIME',)
        # 对比
        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklisthis_result = base.compare_dict(stklisthis_database, stklisthis_excel, 'stklist2022',*stklisthis_ignore)
        custchglog_result = base.compare_dict(custchglog_database, custchglog_excel, 'custchglog', *custchglog_ignore)
        stklistextendhis_result = base.compare_dict(stklistextendhis_database,stklistextendhis_excel,
                                                    'stklistextend2023',*stklistextendhis_ignore)
        # 断言
        final_result =  stklisthis_result+ custchglog_result + stklist_result + stklistextendhis_result
        if not final_result :
            logger().info('股转\定向可转债\兑息\冻结兑息 对比数据无异常')
            assert True
        else:
            logger().error('股转\定向可转债\兑息\冻结兑息 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
