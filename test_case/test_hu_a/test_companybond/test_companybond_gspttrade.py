import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation
from public_method.dbf_operation import creat_new_dbf



class Futures(unittest.TestCase):
    """
    公司债现券交易固定收益平台交易
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['companybond']['gstrade']

    def test_futures(self):
        """
        公司债现券交易固定收益平台交易
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：公司债现券交易固定收益平台交易 准备数据')
        dbf_path = self.yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('dbf文件数据准备完成')
        else:
            logger().error('dbf文件数据准备异常，：{}'.format(dbf_result))
            assert False, dbf_result
        # 创建zqgh文件
        # txt_path = self.yaml['txtPath']
        # txt = TxtOperation(txt_path)
        # txt_result = txt.creat_txt('zqgh')
        # if txt_result is False:
        #     logger().error('zqgh.txt文件创建失败')
        #     assert False, 'zqgh.txt文件创建失败'
        # 执行脚本
        sql_path = self.yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        oracle = OracleDatabase()
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('公司债现券交易固定收益平台交易 准备数据完成')
            assert True
        else:
            logger().error('公司债现券交易固定收益平台交易 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()