import unittest

from config import PathConfig
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.dbf_operation import creat_new_dbf


class EtfIssue(unittest.TestCase):
    """
    沪A\上海ETF发行\T+1日
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_a())['EtfIssue']['T1']

    def test_etf_issue(self):
        """
        沪A\上海ETF发行\T+1日
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪A\上海ETF发行\T+1日 准备数据')
        dbf_path = self.yaml['dbfPath']
        dbf_result = creat_new_dbf(dbf_path)
        if not dbf_result:
            logger().info('沪A\上海ETF发行\T+1日 准备数据完成')
            assert True
        else:
            logger().error('沪A\上海ETF发行\T+1日 准备数据异常')
            assert False, dbf_result


if __name__ == '__main__':
    unittest.main()