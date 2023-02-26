import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    沪A\基金通1.0\持仓对账
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['jijintong1']['stkaudit']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        沪A\基金通1.0\持仓对账
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\基金通1.0\持仓对账 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        fundauditingerror_sql = "select * from fundauditingerror where occurtime>={} and occurtime<={} and  exchid='0' and  stkid " \
                                "in ('519001','519002','519003','519005','519007','519008') ".format(begintime,endtime)

        # 数据库数据
        fundauditingerror_database = base.fundauditingerror_sort(oracle.dict_data(fundauditingerror_sql))

        # Excel数据
        fundauditingerror_excel = base.fundauditingerror_sort(excel.read_excel('fundauditingerror'))

        # 忽略字段
        fundauditingerror_ignore = self.ignore['fundauditingerror']
        # 对比

        fundauditingerror_result = base.compare_dict(fundauditingerror_database, fundauditingerror_excel,
                                                     'fundauditingerror', *fundauditingerror_ignore)

        # 断言
        final_result = fundauditingerror_result
        if not final_result :
            logger().info('沪A\基金通1.0\持仓对账 对比数据无异常')
            assert True
        else:
            logger().error('沪A\基金通1.0\持仓对账 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
