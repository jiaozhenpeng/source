import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation


class Futures(unittest.TestCase):
    """
    智能开平交割
    """
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['intelligent']['delivery']

    def test_futures(self):
        """
        期货市场\智能开平交割
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：智能开平交割 准备数据')
        txt_path = self.yaml['txtPath']
        txt_path2 = self.yaml['txtPath2']
        txt = TxtOperation(txt_path)
        txt2 = TxtOperation(txt_path2)
        # 创建文件
        txt_result = txt.creat_txt('trddata')
        if txt_result is False:
            logger().error('trddata.txt文件创建失败')
            assert False, 'trddata.txt文件创建失败'
        txt_result2 = txt2.creat_txt('delivdetails')
        if txt_result is False:
            logger().error('delivdetails.txt文件创建失败')
            assert False, 'delivdetails.txt文件创建失败'
        sql_path = self.yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        oracle = OracleDatabase()
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('智能开平交割 准备数据完成')
            assert True
        else:
            logger().error('智能开平交割 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()