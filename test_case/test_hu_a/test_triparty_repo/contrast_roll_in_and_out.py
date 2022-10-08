import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastRollinAndOut(unittest.TestCase):
    '''
    对比 上海三方回购\转入转出申报
    '''
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())

    def test_rollin_and_out(self):
        '''
        上海三方回购\转入转出申报数据对比
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 沪A\上海三方回购\转入转出申报 数据')
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        tripartyrepo_inandout = ContrastRollinAndOut().yaml['tripartyrepo_inandout']
        excel_path = tripartyrepo_inandout['excelPath']
        excel = ExcelOperation(excel_path)
        year = BaseAction().get_today_date()[0:4]
        tradinglog = 'tradinglog' + year
        # 查询数据库SQL
        stklist_sql = r'select * from stklist where  exchid = {} and deskid = {} and regid in（{}） and stkid in ({})'.format(
            "'0'", "'00W40'", "'D890008318','D890008279' ", "'010107','010303','142000','010107','142999'")
        tradinglog_sql = r'select * from {}'.format(
            tradinglog) + '  where reckoningtime>={} and reckoningtime<={} and exchid= {} and ' \
                          'acctid in ({}) and briefid in({}) '.format(begintime,
                                                                      endtime,
                                                                      "'0'",
                                                                      "'000890008318','000890008279'",
                                                                      "'005_003_087','005_004_088','005_003_088','005_004_087'")
        stkauditingerror_sql = r'select * from stkauditingerror where businessdate={} and offerregid in({}) and stkid in ({})'.format(
            begintime, "'D890008318','D890008279' ", "'010107','010303','142000','010107'")
        # 需要忽略的字段
        tradinglog_ignore = (
        'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE', 'TRANSACTIONREF')
        stkauditingerror_ignore = ('OCCURTIME', 'KNOCKTIME', 'BUSINESSDATE')
        # 获取数据库数据并排序
        stklist_database = BaseAction().stklist_sort(oracle.dict_data(stklist_sql))
        tradinglog_database = BaseAction().tradinglog_sort(oracle.dict_data(tradinglog_sql))
        stkauditingerror_database = BaseAction().stkauditingerror_sort(oracle.dict_data(stkauditingerror_sql))
        # 获取Excel预期结果并排序
        stklist_excel = BaseAction().stklist_sort(excel.read_excel('stklist'))
        tradinglog_excel = BaseAction().tradinglog_sort(excel.read_excel('tradinglog2022'))
        stkauditingerror_excel = BaseAction().stkauditingerror_sort(excel.read_excel('stkauditingerror'))
        # 对比结果
        stklist_result = BaseAction().compare_dict(stklist_database, stklist_excel, 'stklist')
        tradinglog_result = BaseAction().compare_dict(tradinglog_database, tradinglog_excel, 'tradinglog',
                                                      *tradinglog_ignore)
        stkauditingerror_result = BaseAction().compare_dict(stkauditingerror_database, stkauditingerror_excel,
                                                            'stkauditingerror', *stkauditingerror_ignore)
        # 断言数据是否一致
        if not stklist_result and not tradinglog_result and not stkauditingerror_result:
            logger().info('上海三方回购\转入转出申报数据对比一致')
            assert True
        else:
            logger().error('上海三方回购\转入转出申报数据不一致：{}'.format(stklist_result + tradinglog_result + stkauditingerror_result))
            assert False, stklist_result + tradinglog_result + stkauditingerror_result


if __name__ == '__main__':
    unittest.main()
