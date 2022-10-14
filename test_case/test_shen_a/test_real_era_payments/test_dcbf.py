import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import creat_new_dbf


class DCBF(unittest.TestCase):
    """
    F:\source\用例数据\深A\实时代收付\CDS业务保费支付
    """
    yaml = BaseAction().read_yaml(PathConfig().shen_a())['RealEraPayments']['DCBF']

    def test_DCBF(self):
        """
        F:\source\用例数据\深A\实时代收付\CDS业务保费支付
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：实时代收付\CDS业务保费支付 准备数据')
        dbf_path = self.yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('dbf文件数据准备完成')
        else:
            logger().error('dbf文件数据准备异常，：{}'.format(dbf_result))
            assert False, dbf_result
        sql_path = self.yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        oracle = OracleDatabase()
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('深圳实时代收付\CDS业务保费支付 准备数据完成')
            assert True
        else:
            logger().error('深圳实时代收付\CDS业务保费支付 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()
