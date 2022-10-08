import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastStockTrading(unittest.TestCase):
    yaml = BaseAction().read_yaml(path=PathConfig().shen_a())

    def test_stock_purchase(self):
        '''
        对比股票买入数据
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始对比 深A\股票买卖\股票买入 数据')
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        stock_purchase = ContrastStockTrading().yaml['stockPurchase']
        excel_path = stock_purchase['excelPath']
        account_sql = 'select * from account where currencyid={} and acctid = {} '.format(" '00' ", "'000011728200' ")
        stklist_sql = 'select * from stklist where  exchid = {} and deskid = {} and regid={} and stkid=' \
                      '{}'.format("'1'", "'077011'", "'0117282000'", "'000001'")
        trading_sql = 'select * from tradinglog2022' + '  where reckoningtime>={} and reckoningtime<={} and exchid= {} and ' \
                                                       'acctid={} and briefid={} and stkid={}'.format(begintime,
                                                                                                      endtime,
                                                                                                      "'1'",
                                                                                                      "'000011728200'",
                                                                                                      "'005_001_001'",
                                                                                                      "'000001'")
        contrast_database = {'account': account_sql, 'stklist': stklist_sql, 'tradinglog2021': trading_sql}
        # 对比的sheet表名和需要忽略的字段
        contrast_sheet = {'account': ('DEPOSITSUM',), 'stklist': ('OCCURTIME',),
                          'tradinglog2021': (
                              'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE')}
        assert_result = []
        for key in contrast_database.keys():
            try:
                database_result = oracle.dict_data((contrast_database[key]))
                if database_result:
                    logger().info('获取表：{} 数据成功'.format(key))
                else:
                    assert_result.append('获取表：{} 数据失败或无数据'.format(key))
                    logger().info('获取表：{} 数据失败或无数据'.format(key))
                    continue
                excel_result = ExcelOperation(excel_path).read_excel(key)
                if excel_result:
                    logger().info('获取sheet表：{} 数据成功'.format(key))
                else:
                    assert_result.append('获取表：{} 数据失败或无数据'.format(key))
                    logger().info('获取表：{} 数据失败或无数据'.format(key))
                    continue
                sorted_database_result = BaseAction().sorted_dict(database_result)
                sorted_excel_result = BaseAction().sorted_dict(excel_result)
                # 对比字典里面的数据
                result = BaseAction().compare_dict(sorted_database_result, sorted_excel_result, key,*contrast_sheet[key])
                if not result:
                    continue
                assert_result.append('表：{}，错误：{}'.format(key,result))
            except Exception as e:
                logger().info('{} 表数据对比不一致，错误信息：{}'.format(key, e))
        if not assert_result:
            logger().info('深A\股票买卖\股票买入 数据对比完成，无异常')
            assert True
        else:
            error = '深A\股票买卖\股票买入 数据对比异常，异常信息为：{}'.format(assert_result)
            logger().error(error)
            assert False

    def test_virtual_shareholder_purchase(self):
        '''
        对比 股票买入虚拟股东数据
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深A\股票买卖\股票买入虚拟股东')
        shareholder = ContrastStockTrading().yaml['shareholderPurchase']
        year = str(shareholder['year'])
        excel_path = shareholder['excelPath']
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        account_sql = 'select * from account where currencyid={} and acctid = {} '.format(" '00' ", "'000011728201' ")
        stklist_sql = 'select * from stklist where  exchid = {} and deskid = {} and regid={} and stkid=' \
                      '{}'.format("'1'", "'077011'", "'0117282001'", "'000001'")
        trading_sql = 'select * from tradinglog' + year + '  where reckoningtime>={} and reckoningtime<={} and exchid= {} and ' \
                                                   'acctid={} and briefid={} and stkid={}'.format(begintime, endtime,
                                                                                                  "'1'",
                                                                                                  "'000011728201'",
                                                                                                  "'005_001_001'",
                                                                                                  "'000001'")
        contrast_database = {'account': account_sql, 'stklist': stklist_sql, 'tradinglog2021': trading_sql}
        # 对比的sheet表名和需要忽略的字段
        contrast_sheet = {'account': ('DEPOSITSUM',), 'stklist': ('OCCURTIME',),
                          'tradinglog2021': (
                              'KNOCKTIME', 'SERIALNUM', 'RECKONINGTIME', 'OFFERTIME', 'OCCURTIME', 'SETTLEDATE')}
        assert_result = []
        for key in contrast_database.keys():
            try:
                database_result = oracle.dict_data((contrast_database[key]))
                if database_result:
                    logger().info('获取表：{} 数据成功'.format(key))
                else:
                    assert_result.append('获取表：{} 数据失败或无数据'.format(key))
                    logger().error('获取表：{} 数据失败或无数据'.format(key))
                    continue
                excel_result = ExcelOperation(excel_path).read_excel(key)
                if excel_result:
                    logger().info('获取sheet表：{} 数据成功'.format(key))
                else:
                    assert_result.append('获取表：{} 数据失败或无数据'.format(key))
                    logger().error('获取表：{} 数据失败或无数据'.format(key))
                    continue
                sorted_database_result = BaseAction().sorted_dict(database_result)
                sorted_excel_result = BaseAction().sorted_dict(excel_result)
                # 对比字典里面的数据
                result = BaseAction().compare_dict(sorted_database_result, sorted_excel_result,key, *contrast_sheet[key])
                if not result:
                    continue
                assert_result.append('表：{}，错误：{}'.format(key,result))
            except Exception as e:
                logger().error('{} 表数据对比不一致，错误信息：{}'.format(key, e))

        if not assert_result:
            logger().info('深A\股票买卖\股票买入虚拟股东 数据对比完成，无异常')
            assert True
        else:
            logger().error('深A\股票买卖\股票买入虚拟股东 数据对比异常，异常信息为：{}'.format(assert_result))
            assert  False , assert_result


if __name__ == '__main__':
    unittest.main()
