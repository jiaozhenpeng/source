import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


# 沪A\三方回购转入转出（684，685）
class TripartyRepoInAndOut(unittest.TestCase):

    yaml =  BaseAction().read_yaml(path=PathConfig().hu_a())

    def test_rollin_and_out(self):
        '''
        测试 沪A三方回购转入转出数据准备
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\三方回购\转入转出 准备数据')
        test_yaml = TripartyRepoInAndOut().yaml['tripartyrepo_inandout']
        dbf_path1 = test_yaml['tripartyrepo_inandoutPath']  # 获取转入转出jsmx文件路径
        dbf_path2 = test_yaml['tripartyrepo_inandoutPath2'] # 获取转入转出qtsl文件路径
        dbf_path3 = test_yaml['tripartyrepo_inandoutPath3']  # 获取转入转出zqbd文件路径
        dbf_path4 = test_yaml['tripartyrepo_inandoutPath4'] # 获取转入转出zqye文件路径
        dbf1 = DbfOperation(dbf_path1)
        dbf2 = DbfOperation(dbf_path2)
        dbf3 = DbfOperation(dbf_path3)
        dbf4 = DbfOperation(dbf_path4)
        oracle = OracleDatabase()
        records1 = dbf1.jsmx_file()
        records2 = dbf2.qtsl_file()
        records3 = dbf3.zqbd_file()
        records4 = dbf4.zqye_file()
        dbf1_result = dbf1.creat_dbf(records1, 'jsmx')
        dbf2_result = dbf2.creat_dbf(records2, 'qtsl')
        dbf3_result = dbf3.creat_dbf(records3, 'zqbd')
        dbf4_result = dbf4.creat_dbf(records4, 'zqye')
        if dbf1_result is False or dbf2_result is False or dbf3_result is False or dbf4_result is False :
            assert False,'dbf文件新建失败'
        sql_path = test_yaml['sql']
        sql = BaseAction().read_sql(sql_path)
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('沪A三方回购转入转出数据准备 数据准备完成')
            assert True
        else:
            logger().error('沪A三方回购转入转出数据准备 数据准备失败')
            assert False,oracle_result


if __name__ == '__main__':
    unittest.main()