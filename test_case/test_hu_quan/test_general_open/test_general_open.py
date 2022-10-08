import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation
from public_method.txt_operation import TxtOperation

class GeneralOpen(unittest.TestCase):
    '''
    沪权\普通开仓
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())
    def test_general_opening(self):
        '''
        沪权\普通开仓 准备数据
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\普通开仓 准备数据')
        test_yaml = GeneralOpen().yaml['GeneralOpen']
        txt_path = test_yaml['txtPath']
        sql_path = test_yaml['sqlPath']
        dbf_path = test_yaml['dbfPath']
        txt = TxtOperation(txt_path)
        oracle = OracleDatabase()
        dbf = DbfOperation(dbf_path)
        # 创建文件
        txt_result = txt.creat_txt('trns03')
        if txt_result is False:
            logger().error('trns03.txt文件创建失败')
            assert False, 'trns03.txt文件创建失败'
        dbf_record = dbf.op_jsmx_file()
        dbf_result = dbf.creat_dbf(dbf_record,'op_jsmx')
        if dbf_result is False:
            logger().error('dbf文件创建失败')
            assert False,'dbf文件创建失败'
        sql = BaseAction().read_sql(sql_path)
        sql_result = oracle.update_sql(*sql)
        if not sql_result:
            logger().info('沪权\普通开仓 准备数据完成')
            assert True
        else:
            logger().error('沪权\普通开仓 准备数据异常')
            assert False,sql_result

if __name__ == '__main__':
    unittest.main()