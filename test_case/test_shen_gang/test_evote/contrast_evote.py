import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastBusiness(unittest.TestCase):
    """
    深港\\投票
    """
    yaml = BaseAction().read_yaml(path=PathConfig().shen_gang())['Evote']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())

    def test_shen_business(self):
        '''
        深港\\投票
        :return:
        '''
        logger().info('-------------------------------')
        logger().info('开始执行：深港\\投票 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        # 查询SQL
        exchangemessage_sql = "select * from exchangemessage where exchid={} and messagedate={} and " \
                      "messagetype in('H12','H06')".format('4',str(begintime[:8]))
        votelistinfo_sql = " select * from votelistinfo where basicexchid='SZ_GGT' "
        votestkinfo_sql = " select * from votestkinfo  where basicexchid='SZ_GGT'"
        votemettinginfo_sql = " select * from  votemettinginfo where basicexchid='SZ_GGT' "

        exchangemessage_ignore = ('SERIALNUM','MESSAGEDATE','DATE2','DATE3','OCCURTIME')
        votemettinginfo_ignore = self.ignore['votemettinginfo']
        # 获取数据库数据并排序
        exchangemessage_database = BaseAction().exchangemessage_sort(oracle.dict_data(exchangemessage_sql))
        votelistinfo_database = BaseAction().votelistinfo_sort(oracle.dict_data(votelistinfo_sql))
        votestkinfo_database = BaseAction().votestkinfo_sort(oracle.dict_data(votestkinfo_sql))
        votemettinginfo_database = BaseAction().votemettinginfo_sort(oracle.dict_data(votemettinginfo_sql))

        # 获取excel数据并排序
        exchangemessage_excel = BaseAction().exchangemessage_sort(excel.read_excel('exchangemessage'))
        votelistinfo_excel = BaseAction().votelistinfo_sort(excel.read_excel('votelistinfo'))
        votestkinfo_excel = BaseAction().votestkinfo_sort(excel.read_excel('votestkinfo'))
        votemettinginfo_excel = BaseAction().votemettinginfo_sort(excel.read_excel('votemettinginfo'))
        # 对比数据
        exchangemessage_result = BaseAction().compare_dict(exchangemessage_database,
                                                           exchangemessage_excel, 'exchangemessage',*exchangemessage_ignore)
        votelistinfo_result = BaseAction().compare_dict(votelistinfo_database,votelistinfo_excel, 'votelistinfo')
        votestkinfo_result = BaseAction().compare_dict(votestkinfo_database,votestkinfo_excel,'votestkinfo')
        votemettinginfo_result = BaseAction().compare_dict(votemettinginfo_database,votemettinginfo_excel,
                                                           'votemettinginfo',*votemettinginfo_ignore)
        finalreuslt = exchangemessage_result + votelistinfo_result + votestkinfo_result + votemettinginfo_result
        if not finalreuslt :
            logger().info('深港\\投票T日清算 对比数据无异常')
            assert True
        else:
            logger().error('深港\\投票T日清算 对比数据异常')
            assert False, exchangemessage_result


if __name__ == '__main__':
    unittest.main()
