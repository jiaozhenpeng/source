import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRestrictedShares(unittest.TestCase):
    """
    深A\DVP改革\备付金改革
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['DVP']['BFJGG']

    def test_restricted_shares(self):
        """
        深A\DVP改革\备付金改革
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\DVP改革\备付金改革 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        exchangemessage_sql = " select * from exchangemessage where exchid='1' and messagedate={} and " \
                              "messagetype in('01','03','04')".format(begintime[0:8],)

        # 获取数据库数据并排序

        exchangemessage_database = base.exchangemessage_sort(oracle.dict_data(exchangemessage_sql))
        # 获取excel数据并排序
        exchangemessage_excel = base.exchangemessage_sort(excel.read_excel('exchangemessage'))
        # 可以忽略的字段
        exchangemessage_ignore = ('MESSAGEDATE','PATHDESKID','SERIALNUM','OCCURTIME','DATE1','DATE2')
        # 对比数据
        exchangemessage_result = base.compare_dict(exchangemessage_database, exchangemessage_excel
                                                   , 'exchangemessage',*exchangemessage_ignore)

        final_result =  exchangemessage_result

        # 断言
        if not final_result :
            logger().info('深A\DVP改革\备付金改革 对比数据无异常')
            assert True
        else:
            logger().error('深A\DVP改革\备付金改革 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()