import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.txt_operation import TxtOperation


class FuturesOpen(unittest.TestCase):
    '''
    广期所\智能开平账户开仓 准备数据
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().futures_market())

    def test_futures_opening(self):
        '''
        广期所\智能开平账户开仓 准备数据
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：广期所\智能开平账户开仓 准备数据')
        test_yaml = FuturesOpen().yaml['intelligent']['open']
        txt_path1 = test_yaml['txtPath']
        txt_path2 = test_yaml['txtPath2']
        sql_path = test_yaml['sqlPath']
        txt1 = TxtOperation(txt_path1)
        txt2 = TxtOperation(txt_path2)
        oracle = OracleDatabase()
        # 创建文件
        txt_result1 = txt1.creat_txt('trddata')
        if txt_result1 is False:
            logger().error('trddata.txt文件创建失败')
            assert False, 'trddata.txt文件创建失败'
        txt_result2 = txt2.creat_txt('holddata')
        if txt_result2 is False:
            logger().error('holddata.txt文件创建失败')
            assert False, 'holddata.txt文件创建失败'
        # 执行SQL
        sql = BaseAction().read_sql(sql_path)
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('广期所\智能开平账户开仓 准备数据完成')
            assert True
        else:
            logger().error('广期所\智能开平账户开仓 准备数据失败：{}'.format(oracle_result))
            assert False, oracle_result


if __name__ == '__main__':
    unittest.main()
