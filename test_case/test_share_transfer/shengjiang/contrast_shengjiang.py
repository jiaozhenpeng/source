import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    股转 证券升降层
    """
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())['shengjiang']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        股转 证券升降层
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：股转 证券升降层 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stkinfo_sql = "select * FROM stkinfo where exchid in ('6','9') and stkid in ('874767','871056','989030','989031') "
        stkinfohis_sql = " select * FROM stkinfo{} where occurtime={} and  exchid in ('6','9') and stkid in " \
                         "('874767','871056','989030','989031') ".format(year, begintime)
        stklist_sql = "select * from  stklist where acctid in ('000011721600') and stkid in ('874767','871056','989030','989031') "
        stklisthis_sql = " select * from    stklist{} where occurtime={} and acctid in ('000011721600') and" \
                         " stkid in ('874767','871056','989030','989031')".format(year,begintime)
        stklistextend_sql = "select * FROM stklistextend where acctid in ('000011721600') and stkid " \
                            "in ('874767','871056','989030','989031')"
        stklistextendhis_sql = "select * FROM stklistextend{} where occurtime={} and  acctid in ('000011721600') and stkid " \
                            "in ('874767','871056','989030','989031')".format(year, begintime)
        unprocessedrightsinterests_sql = "select * FROM unprocessedrightsinterests where REGID='GZ11721600' and " \
                                         " stkid in ('874767','871056','989030','989031')"
        custSellLimitTax_sql = "select * FROM custSellLimitTax where exchid in ('6','9') and  acctid in ('000011720611')" \
                               " and stkid in ('874767','871056','989030','989031')"
        custSellLimitTaxhis_sql = "select * FROM custSellLimitTax where exchid in ('6','9') and  acctid in ('000011720611')" \
                               " and stkid in ('874767','871056','989030','989031')"


        # 数据库数据
        stklist_database = base.stklist_sort(oracle.dict_data(stklist_sql))
        stklisthis_database = base.stklist_sort(oracle.dict_data(stklisthis_sql))
        stklistextend_database = base.stklistextend_sort(oracle.dict_data(stklistextend_sql))
        stklistextendhis_database = base.stklistextend_sort(oracle.dict_data(stklistextendhis_sql))
        stkinfo_database = base.stkinfo_sort(oracle.dict_data(stkinfo_sql))
        stkinfohis_database = base.stkinfo_sort(oracle.dict_data(stkinfohis_sql))
        unprocessedrightsinterests_database = base.unprocessedrightsinterests_sort(oracle.dict_data(unprocessedrightsinterests_sql))
        custSellLimitTax_database = base.custSellLimitTax_sort(oracle.dict_data(custSellLimitTax_sql))
        custSellLimitTaxhis_database = base.custSellLimitTax_sort(oracle.dict_data(custSellLimitTaxhis_sql))

        # Excel数据
        stklist_excel = base.stklist_sort(excel.read_excel('stklist'))
        stklisthis_excel = base.stklist_sort(excel.read_excel('stklist2023'))
        stklistextend_excel = base.stklistextend_sort(excel.read_excel('stklistextend'))
        stklistextendhis_excel = base.stklistextend_sort(excel.read_excel('stklistextend2023'))
        stkinfo_excel = base.stkinfo_sort(excel.read_excel('stkinfo'))
        stkinfohis_excel = base.stkinfo_sort(excel.read_excel('stkinfo2023'))
        unprocessedrightsinterests_excel = base.unprocessedrightsinterests_sort(excel.read_excel('unprocessedrightsinterests'))
        custSellLimitTax_excel = base.custSellLimitTax_sort(excel.read_excel('custSellLimitTax'))
        custSellLimitTaxhis_excel = base.custSellLimitTax_sort(excel.read_excel('custSellLimitTaxhis'))
        # 忽略字段
        stklisthis_ignore = self.ignore['stklisthis']
        stklistextendhis_ignore = self.ignore['stklistextendhis']
        stkinfo_ignore = self.ignore['stkinfo']
        stkinfohis_ignore = self.ignore['stkinfohis']

        # 对比

        stklist_result = base.compare_dict(stklist_database, stklist_excel, 'stklist')
        stklisthis_result = base.compare_dict(stklisthis_database, stklisthis_excel, 'stklist2023', *stklisthis_ignore)
        stkinfo_result = base.compare_dict(stkinfo_database,stkinfo_excel,'stkinfo',*stkinfo_ignore)
        stkinfohis_result = base.compare_dict(stkinfohis_database,stkinfohis_excel,'stkinfohis',*stkinfohis_ignore)
        unprocessedrightsinterests_result = base.compare_dict(unprocessedrightsinterests_database,unprocessedrightsinterests_excel,
                                                              'unprocessedrightsinterests')
        custSellLimitTax_reuslt = base.compare_dict(custSellLimitTax_database,custSellLimitTax_excel,'custSellLimitTax')
        custSellLimitTaxhis_result = base.compare_dict(custSellLimitTaxhis_database,custSellLimitTaxhis_excel,'custSellLimitTax')

        # 断言
        final_result =   stklist_result + stklisthis_result + stkinfo_result + stkinfohis_result + \
                         unprocessedrightsinterests_result+ custSellLimitTax_reuslt + custSellLimitTaxhis_result
        if not (final_result and stklist_database):
            logger().info('股转 证券升降层 对比数据无异常')
            assert True
        else:
            logger().error('股转 证券升降层 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
