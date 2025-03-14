import unittest

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction
from public_method.excel_operation import ExcelOperation


class ContrastReserveExercise(unittest.TestCase):
    """
    沪权\行权虚拟股东分配
    """
    yaml = BaseAction().read_yaml(path=PathConfig().hu_quan())['VirtualExer']
    ignore = BaseAction().read_yaml(path=PathConfig().table_ignore())


    def test_reserve_exercise(self):
        """
        沪权\行权虚拟股东分配
        :return:
        """
        logger().info('-------------------------------')
        logger().info('开始执行：沪权\行权虚拟股东分配 对比数据')
        excel_path = self.yaml['excelPath']
        excel = ExcelOperation(excel_path)
        oracle = OracleDatabase()
        begintime = oracle.get_last_update()
        endtime = begintime[0:8] + '235959'
        base = BaseAction()
        year = base.get_today_date()[:4]
        # 查询SQL
        futuretradinglog_sql = "select b.INTERIORDESC,a.* from futuretradinglog{} a ,briefdefine b where" \
                               " a.briefid=b.briefid  and exchid ='X' and stkid in ('11032749','11032748'," \
                               "'11037045','11037044','11037625','11037624','11036245','11036244','11034269'," \
                               "'11036711','10005684','10005685','10005152','10005153') order by stkid,regid," \
                               "serialnum".format(year, begintime,endtime)
        futurepositionhis_sql = "select * from  futureposition{} where exchid ='X' and stkid in ('11032749','11032748'," \
                                "'11037045','11037044','11037625','11037624','11036245','11036244','11034269'," \
                                "'11036711','10005684','10005685','10005152','10005153')".format(year, begintime)
        futurepositiondetailhis_sql = "select * from  futurepositiondetail{} where exchid ='X' and stkid in ('11032749','11032748'," \
                                "'11037045','11037044','11037625','11037624','11036245','11036244','11034269'," \
                                "'11036711','10005684','10005685','10005152','10005153')".format(year, begintime)
        futureposition_sql = "select * from futureposition where  exchid ='X' and stkid in ('11032749','11032748'," \
                             "'11037045','11037044','11037625','11037624','11036245','11036244','11034269','11036711'," \
                             "'10005684','10005685','10005152','10005153') order by stkid,regid "
        futurepositiondetail_sql = "select  * from futurepositiondetail where exchid ='X' and stkid in ('11032749'," \
                                   "'11032748','11037045','11037044','11037625','11037624','11036245','11036244'," \
                                   "'11034269','11036711','10005684','10005685','10005152','10005153') order by stkid,regid"

        unprocessedreckoningresult_sql = "select b.INTERIORDESC,a.* from unprocessedreckoningresult a ,briefdefine b" \
                                         " where a.briefid=b.briefid  and exchid in('X','0')  and  stkid in('11032749'," \
                                         "'11032748','11037045','11037044','11037625','11037624','11036245','11036244'," \
                                         "'11034269','11036711','10005684','10005685','10005152','10005153','510050'," \
                                         "'510180','510500')  and a.briefid in('005_004_054','005_003_054'," \
                                         "'208_002_036','208_001_036') and a.knocktime>={}".format(begintime,)
        unprocessedreckoningresulthis_sql = "select b.INTERIORDESC,a.* from unprocessedreckoningresulthis a ,briefdefine b" \
                                         " where a.briefid=b.briefid  and exchid in('X','0')  and  stkid in('11032749'," \
                                         "'11032748','11037045','11037044','11037625','11037624','11036245','11036244'," \
                                         "'11034269','11036711','10005684','10005685','10005152','10005153','510050'," \
                                         "'510180','510500')  and a.briefid in('005_004_054','005_003_054'," \
                                         "'208_002_036','208_001_036') and a.knocktime>={}".format(begintime,)

        # 获取数据库数据
        futurepositiondetailhis_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetailhis_sql))
        futuretradinglog_database = base.futuretradinglog_sort3(oracle.dict_data(futuretradinglog_sql))
        futurepositionhis_database = base.futureposition_sort(oracle.dict_data(futurepositionhis_sql))
        futureposition_database = base.futureposition_sort(oracle.dict_data(futureposition_sql))
        futurepositiondetail_database = base.futurepositiondetail_sort(oracle.dict_data(futurepositiondetail_sql))
        unprocessedreckoningresult_database = base.unprocessedreckoningresult_sort(oracle.dict_data(unprocessedreckoningresult_sql))
        unprocessedreckoningresulthis_database = base.unprocessedreckoningresulthis_sort(oracle.dict_data(unprocessedreckoningresulthis_sql))

        # excel 数据
        futuretradinglog_excel = base.futuretradinglog_sort3(excel.read_excel('futuretradinglog'))
        futurepositionhis_excel = base.futureposition_sort(excel.read_excel('futureposition2023'))
        futurepositiondetailhis_excel = base.futurepositiondetail_sort(excel.read_excel('futurepositiondetail2023'))
        unprocessedreckoningresult_excel = base.unprocessedreckoningresult_sort(excel.read_excel('unprocessedreckoningresult'))
        unprocessedreckoningresulthis_excel = base.unprocessedreckoningresulthis_sort(excel.read_excel('unprocessedreckoningresulthis'))
        # 忽略字段
        futuretradinglog_ignore = self.ignore['futuretradinglog1']
        futurepositionhis_ignore = self.ignore['futurepositionhis']
        futurepositiondetailhis_ignore = self.ignore['futurepositiondetailhis1']
        unprocessedreckoningresult_ignore = self.ignore['unprocessedreckoningresult']
        unprocessedreckoningresulthis_ignore = self.ignore['unprocessedreckoningresulthis']

        # 对比结果
        futuretradinglog_result = base.compare_dict(futuretradinglog_database, futuretradinglog_excel,
                                                    'futuretradinglog', *futuretradinglog_ignore)
        futurepositionhis_result = base.compare_dict(futurepositionhis_database, futurepositionhis_excel,
                                                     'futureposition2022', *futurepositionhis_ignore)
        futurepositiondetailhis_result = base.compare_dict(futurepositiondetailhis_database,
                                                           futurepositiondetailhis_excel,
                                                           'futurepositiondetail2022', *futurepositiondetailhis_ignore)
        unprocessedreckoningresulthis_result = base.compare_dict(unprocessedreckoningresulthis_database,
                                                                 unprocessedreckoningresulthis_excel,
                                                                 'unprocessedreckoningresulthis',
                                                                 *unprocessedreckoningresulthis_ignore)
        unprocessedreckoningresult_result = base.compare_dict(unprocessedreckoningresult_database,unprocessedreckoningresult_excel
                                                              ,'unprocessedreckoningresult',*unprocessedreckoningresult_ignore)

        # 断言
        final_result = futuretradinglog_result + futurepositionhis_result + futurepositiondetailhis_result\
                       + unprocessedreckoningresult_result + unprocessedreckoningresulthis_result

        if not final_result:
            logger().info('沪权\行权虚拟股东分配 对比数据无异常')
            assert True
        else:
            logger().error('沪权\行权虚拟股东分配 对比数据异常')
            assert False, final_result


if __name__ == '__main__':
    unittest.main()