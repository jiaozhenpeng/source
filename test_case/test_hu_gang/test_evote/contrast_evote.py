import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastBusiness(unittest.TestCase):
    """
    沪港\\投票
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_gang())['Evote']

    def test_shen_business(self):
        logger().info('-------------------------------')
        logger().info('开始执行：沪港\\投票 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        # 查询SQL
        exchangemessage_sql = "select * from exchangemessage where exchid={} and messagedate={} and " \
                      "messagetype in('H12','H06')".format('5',str(begintime[:8]))

        exchangemessage_ignore = ('MESSAGEDATE','OCCURTIME','DATE3','DATE2','SERIALNUM')
        # 获取数据库数据并排序
        exchangemessage_database = BaseAction().exchangemessage_sort(oracle.dict_data(exchangemessage_sql))
        # 获取excel数据并排序
        exchangemessage_excel = BaseAction().exchangemessage_sort(excel.read_excel('exchangemessage'))
        # 对比数据
        exchangemessage_result = BaseAction().compare_dict(exchangemessage_database,
                                                           exchangemessage_excel, 'exchangemessage',*exchangemessage_ignore)

        if not exchangemessage_result :
            logger().info('沪港\\投票T日清算 对比数据无异常')
            assert True
        else:
            logger().error('沪港\\投票T日清算 对比数据异常')
            assert False, exchangemessage_result


if __name__ == '__main__':
    unittest.main()
