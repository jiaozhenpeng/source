import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastGeneralData(unittest.TestCase):
    """
    日终通用数据
    """
    yaml = BaseAction().read_yaml(path=PathConfig().day_end())['GeneralData']

    def test_general_data(self):
        """
        日终通用数据
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：日终通用数据 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        # 查询sql
        unifiedinfiledata_sql = "select * from unifiedinfiledata where DBFID in ('TYZH_F01_YWLS','TYZH_F07_QTZHZL'" \
                                ",'TYZH_F08_QTSYXX','TYZH_F09_QTSDXGL','TYZH_F16_HSTGDZ') and imptime>={}".format(begintime)
        # 数据库数据
        unifiedinfiledata_database = base.unifiedinfiledata_sort(oracle.dict_data(unifiedinfiledata_sql))
        # Excel数据
        unifiedinfiledata_excel = base.unifiedinfiledata_sort(excel.read_excel('UnifiedInFileData'))
        # 忽略字段
        unifiedinfiledata_ignoore = ('FILETIME','OPENDATE','IMPTIME','SERIALNUM','BUSINESSDATE','ORDERTIME',
                                     'INVESTORSBIRTHDAY','GEM_RISKSIGNDATE')
        # 对比
        unifiedinfiledata_result = base.compare_dict(unifiedinfiledata_database, unifiedinfiledata_excel,
                                                     'unifiedinfiledata',*(unifiedinfiledata_ignoore))
        # 断言
        if not unifiedinfiledata_result:
            logger().info('日终通用数据 对比数据无异常')
            assert True
        else:
            logger().error('日终通用数据 对比数据异常')
            assert False, unifiedinfiledata_result


if __name__ == '__main__':
    unittest.main()