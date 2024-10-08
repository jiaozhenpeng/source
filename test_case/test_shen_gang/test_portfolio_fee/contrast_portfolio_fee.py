import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastPortfolioFee(unittest.TestCase):
    """
    深港\证券组合费
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_gang())['PortfolioFee']

    def test_portfolio_fee(self):
        """
        深港\证券组合费
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：深港\证券组合费 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        base = BaseAction()

        # 查询sql
        unprocessedreckoningresult_sql = "select * from unprocessedreckoningresult where EXCHID='4' and DESKID = " \
                                         "'077011' and ORDERTYPE ='TGZH' and REGID in( '0117222000','0117222001')" \
                                         "and knocktime>={}".format(begintime,)
        unprocessedreckoningresulthis_sql = "select * from unprocessedreckoningresulthis where exchid='4' and ORDERTYPE" \
                                            " ='TGZH' and REGID in( '0117222000','0117222001') and knocktime" \
                                            ">={}".format(begintime,)
        # 数据库数据
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(
            oracle.dict_data(unprocessedreckoningresult_sql))
        unprocessedreckoningresulthis_database = base.unprocessedreckoningresulthis_sort(
            oracle.dict_data(unprocessedreckoningresulthis_sql))
        # Excel数据
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(
            excel.read_excel('unprocessedreckoningresult'))
        unprocessedreckoningresulthis_excel = base.unprocessedreckoningresulthis_sort(
            excel.read_excel('unprocessedreckoningresulthis'))
        # 忽略字段
        unprocessedreckoningresult_ignore = ('KNOCKTIME','TRANSACTIONREF','SETTLEDATE','FIRSTCASHSETTLEDATE')
        exchangerights_ignore = ()
        unprocessedreckoningresulthis_ignore = ('KNOCKTIME','TRANSACTIONREF','SETTLEDATE','FIRSTCASHSETTLEDATE')
        # 对比
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,
                                                              unprocessedreckoningresult_excel,
                                                              'unprocessedreckoningresult',
                                                              *unprocessedreckoningresult_ignore)
        unprocessedreckoningresulthis_result = base.compare_dict(unprocessedreckoningresulthis_database,
                                                                 unprocessedreckoningresulthis_excel,
                                                                 'unprocessedreckoningresulthis',
                                                                 *unprocessedreckoningresulthis_ignore)
        # 断言
        final_result = unprocessedreckoningresult_result +  unprocessedreckoningresulthis_result
        if not final_result:
            logger().info('深港\证券组合费 对比数据无异常')
            assert True
        else:
            logger().error('深港\证券组合费 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()
