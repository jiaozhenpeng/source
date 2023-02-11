import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastEtfSplit(unittest.TestCase):
    """
    深银行\兑息\普通兑息\T日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_bank())['dx']['ptdxtday']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_etf_split(self):
        """
        深银行\兑息\普通兑息\T日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深银行\兑息\普通兑息\T日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        lasttradedate = oracle.get_last_update()
        base = BaseAction()
        year = base.get_today_date()[:4]

        # 查询sql
        stkcheckin_sql = "select * from stkcheckin where exchid='B' and stkid in ('102100865','102100866')" \
                         " and occurtime = {}".format(lasttradedate,)

        # 数据库数据
        stkcheckin_database = base.stkcheckin_sort(oracle.dict_data(stkcheckin_sql))

        # Excel数据
        stkcheckin_excel = base.stkcheckin_sort(excel.read_excel('stkcheckin'))

        # 忽略字段
        stkcheckin_ignore = self.ignore['stkcheckin']
        # 对比

        stkcheckin_result = base.compare_dict(stkcheckin_database, stkcheckin_excel, 'stkcheckin',*stkcheckin_ignore)
        # 断言
        final_result =  stkcheckin_result
        if not final_result:
            logger().info('深银行\兑息\普通兑息\T日 对比数据无异常')
            assert True
        else:
            logger().error('深银行\兑息\普通兑息\T日 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
