import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


class GeneralOpenShen(unittest.TestCase):
    '''
    深权\普通开仓
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().shen_quan())

    def test_general_opening(self):
        '''
        深权\普通开仓 准备数据
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深权\普通开仓 准备数据')
        test_yaml = self.yaml['GeneralOpenShen']
        dbf_path1 = test_yaml['dbfPath1']
        dbf_path2 = test_yaml['dbfPath2']
        dbf_path3 = test_yaml['dbfPath3']
        dbf_path4 = test_yaml['dbfPath4']
        dbf_path5 = test_yaml['dbfPath5']
        dbf_path6 = test_yaml['dbfPath6']
        dbf_path7 = test_yaml['dbfPath7']
        dbf_path8 = test_yaml['dbfPath8']
        dbf_path9 = test_yaml['dbfPath9']
        dbf_path10 = test_yaml['dbfPath10']
        dbf_path11 = test_yaml['dbfPath11']
        dbf_path12 = test_yaml['dbfPath12']
        dbf_path13 = test_yaml['dbfPath13']
        dbf_path14 = test_yaml['dbfPath14']
        dbf1 = DbfOperation(dbf_path1)
        dbf2 = DbfOperation(dbf_path2)
        dbf3 = DbfOperation(dbf_path3)
        dbf4 = DbfOperation(dbf_path4)
        dbf5 = DbfOperation(dbf_path5)
        dbf6 = DbfOperation(dbf_path6)
        dbf7 = DbfOperation(dbf_path7)
        dbf8 = DbfOperation(dbf_path8)
        dbf9 = DbfOperation(dbf_path9)
        dbf10 = DbfOperation(dbf_path10)
        dbf11 = DbfOperation(dbf_path11)
        dbf12 = DbfOperation(dbf_path12)
        dbf13 = DbfOperation(dbf_path13)
        dbf14 = DbfOperation(dbf_path14)
        dbf_result1 = dbf1.creat_dbf(dbf1.sjsdz_file(), 'sjsdz')
        dbf_result2 = dbf2.creat_dbf(dbf2.sjsjg_file(), 'sjsjg')
        dbf_result3 = dbf3.creat_dbf(dbf3.sq_bzjmx_file(), 'sq_bzjmx')
        dbf_result4 = dbf4.creat_dbf(dbf4.sq_hycb_file(), 'sq_hycb')
        dbf_result5 = dbf5.creat_dbf(dbf5.sq_hycc_file(), 'sq_hycc')
        dbf_result6 = dbf6.creat_dbf(dbf6.sq_jsmx_file(), 'sq_jsmx')
        dbf_result7 = dbf7.creat_dbf(dbf7.sq_zqje_file(), 'sq_zqje')
        dbf_result8 = dbf8.creat_dbf(dbf8.sjsdz_file(), 'sjsdz')
        dbf_result9 = dbf9.creat_dbf(dbf9.sjsjg_file(), 'sjsjg')
        dbf_result10 = dbf10.creat_dbf(dbf10.sq_bzjmx_file(), 'sq_bzjmx')
        dbf_result11 = dbf11.creat_dbf(dbf11.sq_hycb_file(), 'sq_hycb')
        dbf_result12 = dbf12.creat_dbf(dbf12.sq_hycc_file(), 'sq_hycc')
        dbf_result13 = dbf13.creat_dbf(dbf13.sq_jsmx_file(), 'sq_jsmx')
        dbf_result14 = dbf14.creat_dbf(dbf14.sq_zqje_file(), 'sq_zqje')
        if dbf_result1 is False and dbf_result2 is False and dbf_result3 is False and dbf_result4 is False and \
                dbf_result5 is False and dbf_result6 is False and dbf_result7 is False and dbf_result8 is False \
                and dbf_result9 is False and dbf_result10 is False and dbf_result11 is False and dbf_result12 is False \
                and dbf_result13 is False and dbf_result14 is False:
            logger().error('dbf创建文件失败')
        sql_path = test_yaml['sqlPath']
        sql_path1 = test_yaml['sqlPath1']
        oracle = OracleDatabase()
        sql = BaseAction().read_sql(sql_path)
        sql1 = BaseAction().read_sql(sql_path1)
        sql_result = oracle.update_sql(*sql)
        sql_result1 = oracle.update_sql(*sql1)
        final_result = sql_result + sql_result1
        if not final_result:
            logger().info('深权\普通开仓 准备数据完成')
            assert True
        else:
            logger().error('深权\普通开仓 准备数据异常')
            assert False, sql_result


if __name__ == '__main__':
    unittest.main()
