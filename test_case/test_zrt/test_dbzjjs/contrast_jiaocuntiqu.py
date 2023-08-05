import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastVirtualExer(unittest.TestCase):
    """
    转融通\担保资金结算\交存提取
    """
    yaml = BaseAction().read_yaml(path=PathConfig().zrt())['DBZJJS']['JCTQ']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())


    def test_virtualexer(self):
        """
        转融通\担保资金结算\交存提取
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：转融通\担保资金结算\交存提取 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        shortbegintime = begintime[:8]
        # 查询SQL
        # rc_LendDeskApply_sql = "select * from rc_LendDeskApply where exptime>={} and exptime<={} and lendertype='1' ".format(begintime,endtime)
        tradinglog_sql = "select b.INTERIORDESC,a.* from tradinglog{} a ,briefdefine b where a.briefid=b.briefid  and" \
                         " a.briefid in('002_001_020','002_002_020') and acctid='555000000003' and a.reckoningtime>={} and " \
                         "a.reckoningtime<={} ".format(year,begintime,endtime)

        # 获取数据库数据
        # rc_LendDeskApply_database = base.rc_LendDeskApply_sort(oracle.dict_data(rc_LendDeskApply_sql))
        tradinglog_database = base.tradinglog_sort(oracle.dict_data(tradinglog_sql))

        # excel 数据
        # rc_LendDeskApply_excel = base.rc_LendDeskApply_sort(excel.read_excel('Rc_lenddeskapply'))
        tradinglog_excel = base.tradinglog_sort(excel.read_excel('tradinglog'))
        # 忽略字段
        tradinglog_ignore = self.ignore['tradinglog']

        # 对比结果
        # rc_LendDeskApply_result = base.compare_dict(rc_LendDeskApply_database, rc_LendDeskApply_excel,'rc_LendDeskApply')
        tradinglog_result = base.compare_dict(tradinglog_database,tradinglog_excel,'tradinglog',*tradinglog_ignore)
        # 断言
        final_result =   tradinglog_result

        if not final_result:
            logger().info('转融通\担保资金结算\交存提取 对比数据无异常')
            assert True
        else:
            logger().error('转融通\担保资金结算\交存提取 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()