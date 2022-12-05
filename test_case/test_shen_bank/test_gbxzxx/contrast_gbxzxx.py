import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深银行\广播插入证券信息
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())['gbxzxx']

    def test_etf_split(self):
        """
        深银行\广播插入证券信息
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深银行\广播插入证券信息 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stkinfo_sql = "select * from stkinfo where exchid='B' and stkid in('102002117','061605001') "

        # 数据库数据
        stkinfo_database = base.stkinfo_sort(oracle.dict_data(stkinfo_sql))

        # Excel数据
        stkinfo_excel = base.stkinfo_sort(excel.read_excel('stkinfo'))

        # 忽略字段
        stkinfo_ignore = ('INPUTTIME',)
        # 对比

        stklist_result = base.compare_dict(stkinfo_database, stkinfo_excel, 'stkinfo',*stkinfo_ignore)
        # 断言
        final_result =  stklist_result
        if not final_result:
            logger().info('深银行\广播插入证券信息 对比数据无异常')
            assert True
        else:
            logger().error('深银行\广播插入证券信息 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
