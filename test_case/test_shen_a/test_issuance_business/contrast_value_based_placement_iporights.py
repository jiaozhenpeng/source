import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastValueBasedPlacement(unittest.TestCase):
    """
    深A\发行业务\按值配售\权益发放
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())['IssuanceBusiness']['iporights']

    def test_value_based_placement(self):
        """
        深A\发行业务\按值配售\权益发放
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深A\发行业务\按值配售\权益发放 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        iporights_sql = "select * from iporights where IMPTIME>={}  and offerregid in ( '0117212000' ," \
                                 " '0117252000')  and exchid='1'".format(begintime,)
        # 数据库数据
        iporights_database = base.iporights_sort(oracle.dict_data(iporights_sql))
        # Excel数据
        iporights_excel = base.iporights_sort(excel.read_excel('iporights'))
        # 忽略字段
        iporights_ignore =('IMPUTTIME','RIGHTSDATE','SENDDATE')
        # 对比
        iporights_result = base.compare_dict(iporights_database,iporights_excel,
                                                      'iporights',*iporights_ignore)
        # 断言
        final_result = iporights_result
        if not final_result:
            logger().info('深A\发行业务\按值配售\权益发放 对比数据无异常')
            assert True
        else:
            logger().error('深A\发行业务\按值配售\权益发放 对比数据异常')
            assert False, final_result

if __name__ == '__main__':
    unittest.main()
