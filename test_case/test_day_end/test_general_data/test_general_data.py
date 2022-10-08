

import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import creat_new_dbf


class GeneralData(unittest.TestCase):
    """
    日终通用数据
    """
    yaml = BaseAction().read_yaml(path=PathConfig().day_end())['GeneralData']

    def test_general_data(self):
        """
        日终通用数据
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：日终通用数据 准备数据')
        dbf_path = self.yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('日终通用数据  准备完成')
            assert True
        else:
            logger().error('日终通用数据  准备异常，：{}'.format(dbf_result))
            assert False, dbf_result



if __name__ == '__main__':
    unittest.main()