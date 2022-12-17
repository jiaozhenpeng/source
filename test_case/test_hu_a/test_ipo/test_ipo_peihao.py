import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation
from public_method.dbf_operation import creat_new_dbf



class Futures(unittest.TestCase):
    """
    沪A\按值配售\T日（认购配号日）
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['IPO']['peihao']

    def test_futures(self):
        """
        沪A\按值配售\T日（认购配号日）
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\按值配售\T日（认购配号日） 准备数据')
        # 创建ipogh文件
        txt_path = self.yaml['txtPath']
        txt = TxtOperation(txt_path)
        txt_result = txt.creat_txt('ipogh')
        if txt_result is False:
            logger().error('ipogh.txt文件创建失败')
            assert False, 'ipogh.txt文件创建失败'
        # 执行脚本
        sql_path = self.yaml['sqlPath']
        sql = BaseAction().read_sql(sql_path)
        oracle = OracleDatabase()
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('沪A\按值配售\T日（认购配号日） 准备数据完成')
            assert True
        else:
            logger().error('沪A\按值配售\T日（认购配号日） 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()