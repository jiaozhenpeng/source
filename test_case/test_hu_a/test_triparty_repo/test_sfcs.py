import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


# 沪A\三方回购初始交易（680）
class TripartyReposfcs(unittest.TestCase):

    yaml =  BaseAction().read_yaml(path=PathConfig().hu_a())

    def test_tripartyreposfcs(self):
        '''
        测试 沪A三方回购初始交易数据准备
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\三方回购\转入转出')
        test_yaml = TripartyReposfcs().yaml['TripartyReposfcs']
        dbf_path1 = test_yaml['tripartyrepo_sfcsPath']  # 获取初始交易jsmx文件路径
        dbf_path2 = test_yaml['tripartyrepo_sfcsPath2'] # 获取初始交易qtsl文件路径
        dbf_path3 = test_yaml['tripartyrepo_sfcsPath3']  # 获取初始交易zqbd文件路径
        dbf_path4 = test_yaml['tripartyrepo_sfcsPath4'] # 获取初始交易zqye文件路径
        dbf1 = DbfOperation(dbf_path1)
        dbf2 = DbfOperation(dbf_path2)
        dbf3 = DbfOperation(dbf_path3)
        dbf4 = DbfOperation(dbf_path4)
        oracle = OracleDatabase()
        records1 = dbf1.jsmx_file()
        records2 = dbf2.qtsl_file()
        records3 = dbf3.zqbd_file()
        records4 = dbf4.zqye_file()
        dbf1.creat_dbf(records1, 'jsmx')
        dbf2.creat_dbf(records2, 'qtsl')
        dbf3.creat_dbf(records3, 'zqbd')
        dbf4.creat_dbf(records4, 'zqye')
        sql_path = test_yaml['sql']
        sql = BaseAction().read_sql(sql_path)
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('沪A三方回购初始交易数据准备 数据准备完成')
            assert True
        else:
            logger().error('沪A三方回购初始交易数据准备 数据准备失败')
            assert False,oracle_result

if __name__ == '__main__':
    unittest.main()




if __name__ == '__main__':
    unittest.main()