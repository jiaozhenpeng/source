import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation, creat_new_dbf


# 深A\协议回购
class Repo(unittest.TestCase):

    yaml =  BaseAction().read_yaml(path=PathConfig().shen_a())

    def test_repo(self):
        '''
        测试 深A\协议回购\T日  准备数据
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深A\协议回购\T日')
        test_yaml = Repo().yaml['repo']
        dbf_path = test_yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('dbf文件数据准备完成')
        else:
            logger().error('dbf文件数据准备异常，：{}'.format(dbf_result))
            assert False, dbf_result
        sql_path = test_yaml['sql']
        oracle = OracleDatabase()
        sql = BaseAction().read_sql(sql_path)
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('深A\协议回购\T日 数据准备完成')
            assert True
        else:
            logger().error('深A\协议回购\T日 数据准备失败')
            assert False,'sql执行错误，数据准备失败'
if __name__ == '__main__':
    unittest.main()