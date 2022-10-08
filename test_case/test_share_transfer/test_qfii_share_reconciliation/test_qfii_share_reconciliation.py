import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


class QfiiShareReconciliation(unittest.TestCase):
    '''
    股转\QFII股份对账
    '''
    yaml = BaseAction().read_yaml(PathConfig().share_reconciliation())
    def test_share_reconciliation(self):
        '''
        股转\QFII股份对账准备数据
        :return:
        '''
        logger().info('---------------------')
        logger().info('股转\QFII股份对账 准备数据开始')
        test_yaml = QfiiShareReconciliation().yaml['QfiiShareReconciliation']
        dbf_path  = test_yaml['dbfPath']
        sql_path = test_yaml['sqlPath']
        dbf = DbfOperation(dbf_path)
        oracle = OracleDatabase()
        records = dbf.bjsjg_file()
        dbf_result = dbf.creat_dbf(records,'bjsjg')
        if dbf_result is False:
            return False,'dbf文件新建失败'
        sql = BaseAction().read_sql(sql_path)
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('股转\QFII股份对账 数据准备完成')
            assert True
        else:
            logger().error('股转\QFII股份对账 数据准备失败')
            assert False,oracle_result

if __name__ == '__main__':
    unittest.main()