import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastQfiiShareReconciliation(unittest.TestCase):
    '''
    对比股转\QFII股份对账
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().share_reconciliation())['QfiiShareReconciliation']

    def test_share_reconciliation(self):
        '''
        对比股转\QFII股份对账
        :return:
        '''
        logger().info('-------------------------')
        logger().info('开始对比  股转\QFII股份对账 数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询数据SQL
        stkauditingerror_sql = " select * from stkauditingerror where businessdate={} and offerregid ='GZ11721400' and" \
                               " stkid in ('400001','400006','400008','400009')".format(begintime)
        # 需要忽略的字段
        stkauditingerror_ignore = ('OCCURTIME', 'KNOCKTIME', 'BUSINESSDATE')
        # 获取数据库数据并排序
        stkauditingerror_database = BaseAction().stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))
        # 获取Excel数据并排序
        stkauditingerror_excel = BaseAction().stkauditingerror_sort(excel.read_excel('stkauditingerror'))
        # 对比数据
        stkauditingerror_result = BaseAction().compare_dict(stkauditingerror_database, stkauditingerror_excel,
                                                            'stkauditingerror', *(stkauditingerror_ignore))
        if not stkauditingerror_result:
            logger().info('股转\QFII股份对账 数据对比无异常')
            assert True
        else:
            logger().error('股转\QFII股份对账 数据对比异常:{}'.format(stkauditingerror_result))
            assert False, stkauditingerror_result

    if __name__ == '__main__':
        unittest.main()
