import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation


class FuturesOpen(unittest.TestCase):
    '''
    按配置分配子账户 准备数据
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())['reg_product']

    def test_futures_opening(self):
        '''
        按配置分配子账户 准备数据

        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：期货市场\按配置分配子账户 准备数据')
        trddata = self.yaml['trddataPath']
        opttrddata = self.yaml['opttrddataPath']
        sql_path = self.yaml['sqlPath']
        txt = TxtOperation(trddata)
        txt2 = TxtOperation(opttrddata)
        oracle = OracleDatabase()
        # 创建trddata文件
        txt_result = txt.creat_txt('trddata')
        if txt_result is False:
            logger().error('trddata.txt文件创建失败')
            assert False, 'trddata.txt文件创建失败'
        # 创建opttrddata文件
        txt_result = txt2.creat_txt('opttrddata')
        if txt_result is False:
            logger().error('opttrddata.txt文件创建失败')
            assert False, 'opttrddata.txt文件创建失败'

        # 执行SQL
        sql = BaseAction().read_sql(sql_path)
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('期货市场\按配置分配子账户 准备数据完成')
            assert True
        else:
            logger().error('期货市场\按配置分配子账户 准备数据失败：{}'.format(oracle_result))
            assert False, oracle_result


if __name__ == '__main__':
    unittest.main()
