import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation


class OffsetMargin(unittest.TestCase):
    """
    期货市场\custfund
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['custfund']

    def test_offset_margin(self):
        """
        期货市场\custfund
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：期货市场\custfund 准备数据')
        txt_path = self.yaml['txtPath']
        txt = TxtOperation(txt_path)
        # 创建文件
        txt_result = txt.creat_txt('cusfund')
        if txt_result is False:
            logger().error('cusfund.txt文件创建失败')
            assert False, 'cusfund.txt文件创建失败'
        # sql_path = self.yaml['sqlPath']
        # sql = BaseAction().read_sql(sql_path)
        # oracle = OracleDatabase()
        # sql_result = oracle.update_sql(*sql)
        # if not sql_result:
        #     logger().info('期货市场\custfund 准备数据完成')
        #     assert True
        # else:
        #     logger().error('期货市场\custfund 准备数据异常')
        #     assert False, sql_result


if __name__ == '__main__':
    unittest.main()
