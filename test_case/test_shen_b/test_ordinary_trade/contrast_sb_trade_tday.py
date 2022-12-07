import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastOrdinaryTransaction(unittest.TestCase):
    """
    深B\普通交易\普通交易\T日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_b())['OrdinaryTrade']['Tday']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())


    def test_ordinary_transaction(self):
        """
        深B\普通交易\普通交易\T日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深B\普通交易\普通交易\T日 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        # 查询SQL

        unprocessedreckoningresulthis_sql = "select * from unprocessedreckoningresulthis where EXCHID='3' and STKID " \
                                            "in ('200026','200030') and REGID in " \
                                            "('0000SB3522','0000888888')  and knocktime>={}".format(begintime,)
        unprocessedreckoningresult_sql = "select * from unprocessedreckoningresult where EXCHID='3' and STKID " \
                                         "in ('200026','200030') and REGID in " \
                                         "('0000SB3522','0000888888') and knocktime>={}".format(begintime,)
        stklist_sql = "select * from STKLIST where EXCHID = '3' and REGID in( '0000SB3522','0000888888') and STKID" \
                      " in ('200026','200030') "
        # 获取数据库数据并排序

        unprocessedreckoningresulthis_database = BaseAction().unprocessedreckoningresulthis_sort(
            oracle.dict_data(unprocessedreckoningresulthis_sql))
        unprocessedreckoningresult_database = BaseAction().unprocessedreckoningresult_sort(
            oracle.dict_data(unprocessedreckoningresult_sql))
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        # 获取excel数据并排序
        unprocessedreckoningresulthis_excel = BaseAction().unprocessedreckoningresulthis_sort(
            excel.read_excel('unprocessedreckoningresulthis'))
        unprocessedreckoningresult_excel = BaseAction().unprocessedreckoningresult_sort(
            excel.read_excel('unprocessedreckoningresult'))
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        # 可以忽略的字段
        unprocessedreckoningresulthis_ignore = self.ignore['unprocessedreckoningresulthis']
        unprocessedreckoningresult_ignore = self.ignore['unprocessedreckoningresult']
        stklist_ignore = ()
        # 对比数据

        unprocessedreckoningresulthis_result = BaseAction().compare_dict(unprocessedreckoningresulthis_database,
                                                                         unprocessedreckoningresulthis_excel,
                                                                         'unprocessedreckoningresulthis',
                                                                         *unprocessedreckoningresulthis_ignore)
        unprocessedreckoningresult_result = BaseAction().compare_dict(unprocessedreckoningresult_database,
                                                                      unprocessedreckoningresult_excel,
                                                                      'unprocessedreckoningresult',
                                                                      *unprocessedreckoningresult_ignore)
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        final_result =  unprocessedreckoningresulthis_result + unprocessedreckoningresult_result + stklist_result
        if not final_result:
            logger().info('深B\普通交易\普通交易\T日 对比数据无异常')
            assert True
        else:
            logger().error('深B\普通交易\普通交易\T日 对比数据异常')
            assert False,final_result
if __name__ == '__main__':
    unittest.main()