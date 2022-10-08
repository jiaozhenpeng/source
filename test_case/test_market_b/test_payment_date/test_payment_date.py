import unittest
from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import DbfOperation


class PaymentDate(unittest.TestCase):
    '''
    市场B\冻结变更和冻结结息\兑付冻结解冻
    '''
    yaml = BaseAction().read_yaml(PathConfig().market_b())
    def test_payment_date(self):
        '''
        市场B\冻结变更和冻结结息\兑付冻结解冻
        :return:
        '''
        logger().info('------------------')
        logger().info('开始执行 市场B\冻结变更和冻结结息\兑付冻结解冻日 准备数据')
        test_yaml = PaymentDate().yaml['PaymentDate']
        dbf_path = test_yaml['dbfPath']
        dbf_path1 = test_yaml['dbfPath1']
        dbf_path2 = test_yaml['dbfPath2']
        dbf_path3 = test_yaml['dbfPath3']
        sqlPath = test_yaml['sqlPath']
        dbf = DbfOperation(dbf_path)  # 初始化dbf
        dbf1 = DbfOperation(dbf_path1)
        dbf2 = DbfOperation(dbf_path2)
        dbf3= DbfOperation(dbf_path3)
        oracle = OracleDatabase()
        records = dbf.szyh_sjsgb_file()  # 获取原有dbf文件数据并修改日期
        records1 = dbf1.szyh_sjsjg_file()
        records2 = dbf2.szyh_sjsqs_file()
        records3 = dbf3.szyh_sjszj_file()
        sql = BaseAction().read_sql(sqlPath)
        dbf_result = dbf.creat_dbf(records, 'szyh_sjsgb')
        dbf1_result = dbf1.creat_dbf(records1, 'szyh_sjsjg')
        dbf2_result = dbf2.creat_dbf(records2, 'szyh_sjsqs')
        dbf3_result = dbf3.creat_dbf(records3, 'szyh_sjszj')
        if dbf_result is False or dbf1_result is False or dbf2_result is False or dbf3_result is False:
            assert False,'文件新建失败'
        oracle_result = oracle.update_sql(*sql)
        if not oracle_result:
            logger().info('市场B\冻结变更和冻结结息\兑付冻结解冻 准备数据完成')
            assert True
        else:
            logger().error('市场B\冻结变更和冻结结息\兑付冻结解冻 准备数据失败')
            assert False, oracle_result

    if __name__ == '__main__':
        unittest.main()

