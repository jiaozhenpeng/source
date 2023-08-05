import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastVirtualExer(unittest.TestCase):
    """
    转融通\出借人资料报备
    """
    yaml = BaseAction().read_yaml(path=PathConfig().zrt())['CJRZLBBQR']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())


    def test_virtualexer(self):
        """
        转融通\出借人资料报备
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：转融通\出借人资料报备 对比数据')
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
        rc_Lender_sql = "select * from  rc_Lender where offerregid in('A117212000','0117212000','A117202000','0117202000'" \
                        ",'A117222000','0117222000','A117252000','0117252000') "

        # 获取数据库数据
        # rc_LendDeskApply_database = base.rc_LendDeskApply_sort(oracle.dict_data(rc_LendDeskApply_sql))
        rc_Lender_database = base.rc_Lender_sort(oracle.dict_data(rc_Lender_sql))

        # excel 数据
        # rc_LendDeskApply_excel = base.rc_LendDeskApply_sort(excel.read_excel('Rc_lenddeskapply'))
        rc_LendDer_excel = base.rc_Lender_sort(excel.read_excel('rc_lender'))
        # 忽略字段
        rc_lender_ignore = self.ignore['rc_lender']

        # 对比结果
        # rc_LendDeskApply_result = base.compare_dict(rc_LendDeskApply_database, rc_LendDeskApply_excel,'rc_LendDeskApply')
        rc_LendDer_result = base.compare_dict(rc_Lender_database,rc_LendDer_excel,'rc_LendDer',*rc_lender_ignore)
        # 断言
        final_result =   rc_LendDer_result

        if not final_result:
            logger().info('转融通\出借人资料报备 对比数据无异常')
            assert True
        else:
            logger().error('转融通\出借人资料报备 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()