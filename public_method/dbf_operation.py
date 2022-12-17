import os
import shutil
from datetime import datetime

import dbf

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction


class DbfOperation():
    """
    读写dbf文件
    """
    t = OracleDatabase().get_trade_date()
    t1 = OracleDatabase().get_trade_date(1)
    t2 = OracleDatabase().get_trade_date(2)
    t3 = OracleDatabase().get_trade_date(3)
    t5 = OracleDatabase().get_trade_date(5)
    lasttradedate1 = OracleDatabase().get_last_trade_date(1)

    def __init__(self, path):
        self.dbf_file = dbf.Table(path, codepage='cp936')

    def creat_dbf(self, records, filename):
        """
        传入需要导入的数据列表和新文件名称，生成新的dbf文件
        :param records:
        :param filename:
        :return: bool
        """
        filename = filename + '.dbf'
        dbf_config = BaseAction().read_yaml(path=PathConfig().dbf())
        path = os.path.join(dbf_config['savePath'], self.t)
        if os.path.exists(path) is False:
            os.mkdir(path)
            logger().info('创建路径：{}'.format(path))
        file_path = os.path.join(dbf_config['getPath'], filename)
        new_file_path = os.path.join(path, filename)
        if os.path.exists(new_file_path) is False:
            shutil.copy(file_path, new_file_path)
            logger().info('新文件生成，生成路径：{}'.format(new_file_path))
        table = dbf.Table(new_file_path).open(mode=dbf.READ_WRITE)
        try:
            for record in records:
                if '_NULLFLAGS' in record:
                    del record['_NULLFLAGS']
                    logger().info('删除字段：_NULLFLAGS ')
                table.append(record)
            logger().info('文件数据添加成功:{}'.format(filename))
            table.close()
            return True
        except Exception as e:
            logger().info('文件数据添加失败:{}，错误信息{}'.format(filename, e))
            return False

    def delete_record(self):
        """
        清除dbf文件数据
        :return:
        """
        self.dbf_file.open(mode=dbf.READ_WRITE)
        while True:
            if not self.dbf_file:  # 判断是否有数据，没有数据结束循环
                break
            dbf.delete(self.dbf_file[0])
            self.dbf_file.pack()
        self.dbf_file.close()

    def get_data(self, **kwargs):
        """
        修改部分字段，字典格式传入对应的修改字段和修改后字段值，并返回修改后的文件数据列表
        :param kwargs:
        :return: [{},...]
        """
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                for key in kwargs.keys():
                    # logger().info('修改字段{}，修改前是:{},修改后为：{}'.format(key, rec[key], kwargs[key]))
                    rec[key] = kwargs[key]
            records.append(record)
        table.close()
        return records

    def replace_time(self, time1, time2):
        """
        time1是<class 'datetime.date'>类型，time2是字符串类型的日期（20220101），替换time1中的年月日为time2
        :param time1:
        :param time2:
        :return:
        """
        year = int(time2[:4])
        month = int(time2[4:6])
        day = int(time2[6:])
        return time1.replace(year, month, day)

    def gh_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(BCRQ=cjrq)

    def bgh_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(BCRQ=cjrq)

    def dgh_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(BCRQ=cjrq)

    def zqy_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(DJRQ=self.lasttradedate1)

    def abcsj_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(TZRQ=cjrq)

    def ywhb_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['YWLX'] in ('419','830', '831'):  # 只有sbrq(申报日期)需要变更，419的RQ为减持日期
                    rec['SBRQ'] = cjrq
            records.append(record)
        table.close()
        return records

    def jsmx_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['JYRQ'], rec['QSRQ'], rec['JSRQ'] = cjrq, qsrq, jsrq  # 011,037
                if rec['YWLX'] in ('691', '605', '684', '685','692','693'):  # 根据业务类型判断，交易日期、清算日期、交收日期都是T日
                    rec['JSRQ'] = cjrq
                elif rec['YWLX'] in ('680', ):  # 根据业务类型判断jsrq
                    if rec['SQBH'] in ('70','77','79','80'):
                        rec['QTRQ'] = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%Y%m%d')
                    elif rec['SQBH'] in ('72','74'):
                        rec['QTRQ'] = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y%m%d')
                    elif rec['SQBH'] in ('76',):
                        rec['QTRQ'] = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y%m%d')
                    elif rec['SQBH'] in ('36',):
                        rec['QTRQ'] = (datetime.date.today() + datetime.timedelta(days=184)).strftime('%Y%m%d')
                if rec['YWLX'] in ('655', '656'):  # 根据业务类型判断jsrq
                    rec['JSRQ'] = self.t
                if rec['YWLX'] in ('419', ):  # 419股息红利税，无交易日期
                    rec['JYRQ'] = None
            records.append(record)
        table.close()
        return records

    def jsmx03_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:

                rec['JYRQ'], rec['QSRQ'], rec['JSRQ'] = cjrq, qsrq, jsrq  # 011,
                if rec['YWLX'] in ('691', '605', '684', '685'):  # 根据业务类型判断jsrq
                    rec['JSRQ'] = cjrq
                    rec['QTRQ'] = self.t
                if rec['YWLX'] in ('680', '681'):  # 根据业务类型判断jsrq
                    rec['QTRQ'] = self.t
                if rec['YWLX'] in ('655', '656'):  # 根据业务类型判断jsrq
                    rec['JSRQ'] = self.t

            records.append(record)
        table.close()
        return records

    def jsmx02_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['JYRQ'], rec['QSRQ'], rec['JSRQ'] = cjrq, qsrq, jsrq
                records.append(record)
        table.close()
        return records


    def wdq_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['CJRQ'] = self.t
                if rec['WDQLB'] in ('008', ):  # 根据业务类型判断jsrq
                    if rec['CJXLH'] in ('70','77','79','80'):
                        rec['QTRQ'] = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%Y%m%d')
                    elif rec['CJXLH'] in ('72','74'):
                        rec['QTRQ'] = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y%m%d')
                    elif rec['CJXLH'] in ('76',):
                        rec['QTRQ'] = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y%m%d')
                    elif rec['CJXLH'] in ('36',):
                        rec['QTRQ'] = (datetime.date.today() + datetime.timedelta(days=184)).strftime('%Y%m%d')
            records.append(record)
        table.close()
        return records

    # 处理lofmxzf文件，除转托管转入外，其他成交日期小于确认日期
    def lofmxzf_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.lasttradedate1
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:

                rec['FSRQ'], rec['QRRQ'], rec['CJRQ'] = qsrq, qsrq, cjrq
                if rec['BZSM'] == '645':  # 场外转场内，发送日期、确认日期、成交日期相同
                    rec['CJRQ'] = qsrq
            records.append(record)
        table.close()
        return records

    # 处理cil文件，
    def cil_kj_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.lasttradedate1
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['ZJLX'] == '02':  # 02基金收益的成交日期交收日期都为当日
                    rec['JSRQ'],rec['JYRQ'] = qsrq, qsrq
            records.append(record)
        table.close()
        return records

    # 处理cil文件，
    def cil_ks_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.lasttradedate1
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['ZJLX'] == '02':  # 02基金收益的成交日期交收日期都为当日
                    rec['JSRQ'],rec['JYRQ'] = qsrq, qsrq
            records.append(record)
        table.close()
        return records

        # 处理cil文件，

    def etftbk_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.lasttradedate1
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['ZJLX'] == '203':  # 203基金收益的成交日期交收日期都为当日
                    rec['JSRQ'], rec['JYRQ'] = qsrq, qsrq
            records.append(record)
        table.close()
        return records

    # 处理其他数量
    def qtsl_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['SJLX'] == '018':
                    rec['RQ'] = self.t1
                else:
                    rec['RQ'] = self.t  #020,锁定得最后一次变化  022
            records.append(record)
        table.close()
        return records

    def zqye_file(self, jzrq=None):
        if jzrq == None:
            jzrq = self.t
        return self.get_data(JZRQ=jzrq)

    def zqbd_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(BDRQ=cjrq)


    def zjhz_file(self, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['QSBZ'] in ('01D','01A','01B','01C','01E' ):  # 根据清算标志判断jsrq
                    rec['QSRQ'],rec['JSRQ'] = self.t,self.t
            records.append(record)
        table.close()
        return records

    def zjbd_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(FSRQ=cjrq)

    def sjmx1_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param :
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        return self.get_data(MXCJRQ=cjrq, MXQSRQ=qsrq, MXJSRQ=jsrq, MXFSRQ=fsrq)

    def sjsgb_file(self, cjrq=None, jsrq=None, nextTwoDay=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param :
        :return:
        """
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        if cjrq is None:
            cjrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if nextTwoDay is None:
            nextTwoDay = OracleDatabase().get_trade_date(2)
        for record in table:
            with record as rec:
                logger().info('修改字段{}，修改前是:{},修改后为：{}'.format('GBRQ', rec['GBRQ'], cjrq))
                rec['GBRQ'] = cjrq
                if rec['GBLB'] in ('QP',):
                    rec['GBRQ1'], rec['GBRQ2'] = cjrq, cjrq
                elif rec['GBLB'] in ('LX',):
                    rec['GBRQ1'], rec['GBRQ2'] = cjrq, jsrq  # 计息起始日和截止日，随便写的
                elif rec['GBLB'] in ('MZ',):  # 面值适用日期，下一交易日
                    rec['GBRQ1'] = jsrq
                elif rec['GBLB'] in ('FX',):  # 发行的权益日期，T-2
                    rec['GBRQ1'] = OracleDatabase().get_last_trade_date(2)
                elif rec['GBLB'] in ('ZS',):  # 折算率起始日期和截止日期，下两个交易日
                    rec['GBRQ1'], rec['GBRQ2'] = nextTwoDay, nextTwoDay
            records.append(record)
        table.close()
        return records

    # 处理lofjs文件，除转托管转入外，其他成交日期小于确认日期
    def lofjs_file(self, cjrq=None, qsrq=None, jsrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.lasttradedate1
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['JSYWLB'] in('TA11','TA12','TA21' ,'TA22') :#TA11,TA12,TA21 ,TA222委托日期和发送日期相同，过户日期无效
                    rec['JSWTRQ'], rec['JSFSRQ'] = qsrq, qsrq
                if rec['JSYWLB'] in('TA13','TA23') : #
                    rec['JSWTRQ'], rec['JSFSRQ'] = cjrq, qsrq
            records.append(record)
        table.close()
        return records


    def szyh_sjsgb_file(self, cjrq=None, jsrq=None, nextTwoDay=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param :
        :return:
        """
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        if cjrq is None:
            cjrq = self.t
        for record in table:
            with record as rec:
                rec['GBRQ'] = cjrq
                if rec['GBLB'] == 'QP' and rec['GBDM2'] == 'X': #交易所测试给的兑息是登记日是当日，到账日是下一日
                    rec['GBRQ1'] ,rec['GBRQ2']= cjrq, self.t1
                elif rec['GBLB'] == 'QP' and rec['GBDM2'] == 'D': #交易所测试给的兑付登记日和到账日都是当日
                    rec['GBRQ1'], rec['GBRQ2'] = cjrq, cjrq
            records.append(record)
        table.close()
        return records

    # 发行可申购额度信息库
    def sjsks_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['KSFSRQ'] = self.replace_time(rec['KSFSRQ'], self.t)
            records.append(record)
        table.close()
        return records

    def sjszj_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(ZJJZRQ=cjrq)

    def szyh_sjszj_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(ZJJZRQ=cjrq)

    def szyh_sjsdz_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(DZFSRQ=cjrq)

    def szyh_sjsfw_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(FWCLRQ=cjrq,FWFSRQ= cjrq)

    def sjstj_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(TJCJRQ=cjrq)

    def sjsjg_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None, qtrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['JGQTRQ'].replace(' ', '') and rec['JGCJRQ'].replace(' ',
                                                                            ''):  # 只有其他日期和交易日期都存在时，才会计算其他日期和交易日期的差值
                    temp = datetime.strptime(rec['JGQTRQ'], '%Y%m%d') - datetime.strptime(rec['JGCJRQ'],
                                                                                          '%Y%m%d') + datetime.strptime(
                        cjrq, '%Y%m%d')
                    tempdate = temp.strftime('%Y%m%d')
                # FJ01 成交日期 、清算日期、发送日期 = T日，交收日期为T+1,其他日期为空
                rec['JGCJRQ'], rec['JGQSRQ'], rec['JGJSRQ'], rec['JGFSRQ'], rec['JGQTRQ'] = cjrq, qsrq, jsrq, fsrq, qtrq
                if rec['JGYWLB'] == 'XYCS':  # 协议初始
                    rec['JGQTRQ'] = tempdate
                elif rec['JGYWLB'] == 'XYHY':  # 协议合约
                    rec['JGQSRQ'], rec['JGJSRQ'], rec['JGQTRQ'] = None, None, tempdate
                elif rec['JGYWLB'] in (
                        'DJBG', 'DJ00','FGS6','FGSD', 'ZTZC', 'ZTZR', 'ZTXS', 'ZTTZ', 'ZJQ0', 'ZJQ1', 'ZJQ2', 'TGZX', 'FJZG',
                        'TZGF', 'GS4B', 'GSSG', 'XGJX', 'XGXS', 'ZQZH', 'ZQZD',
                        'ZQZZ','TG20','TG21','TG22','TG23') or (rec['JGYWLB'] == 'ZQKZ' and rec['JGJSSL'] > 0):
                    # 清算日期和交收日期和其他日期为空，成交日期、发送日期= T日
                    rec['JGQSRQ'], rec['JGJSRQ'], rec['JGQTRQ'] = None, None, None
                elif rec['JGYWLB'] in ('QQSD',):  # 成交日期,其他日期为空，清算日期、交收日期、发送日期 = T日
                    rec['JGCJRQ'], rec['JGJSRQ'], rec['JGQTRQ'] = None, cjrq, None
                elif rec['JGYWLB'] in ('QP90','TG90'):  # 发送日期 = T日,其他日期都是空
                    rec['JGCJRQ'], rec['JGJSRQ'], rec['JGQSRQ'],rec['JGQTRQ'] = None, None, None, None
                elif rec['JGYWLB'] in ('CSTZ','CSXX','CSXX'):   #RTGS交收的，四个日期为T日，其他日期空
                    rec['JGJSRQ'],rec['JGQTRQ'] = cjrq,None
            records.append(record)
        table.close()
        return records

    def szyh_sjsjg_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None, qtrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['JGYWLB'] in('JY03','QPPX','QPDF','DJDJ') :
                    rec['JGCJRQ'], rec['JGQSRQ'], rec['JGJSRQ'], rec['JGFSRQ'] = cjrq, qsrq, qsrq, fsrq
                elif rec['JGYWLB'] in('TGZX','DJ00','DJBG') :
                    rec['JGCJRQ'], rec['JGFSRQ'] = cjrq, fsrq
            records.append(record)
        table.close()
        return records


    def szyh_sjsmx0_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None, qtrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['MXYWLB'] in('JY03','') :
                    rec['MXCJRQ'], rec['MXQSRQ'], rec['MXJSRQ'], rec['MXFSRQ'] = cjrq, qsrq, qsrq, fsrq
            records.append(record)
        table.close()
        return records


    def sjsmx2_file(self, qsrq=None, jsrq=None, fsrq=None):
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['MXYWLB'] == 'BG1C':
                    rec['MXQSRQ'] ,rec['MXCJRQ'] ,rec['MXFSRQ'] = qsrq,qsrq,fsrq
                    rec['MXJSRQ'],rec['MXQTRQ'] = self.t3,self.t3
                elif rec['MXYWLB'] == 'CSFY':
                    rec['MXCJRQ'],rec['MXQSRQ'],rec['MXJSRQ'],rec['MXFSRQ'] = qsrq,qsrq,jsrq,fsrq

            records.append(record)
        table.close()
        return records

    def sjsmx0_file(self, qsrq=None, jsrq=None, fsrq=None):
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['MXYWLB'] in ('CSTZ','CSXX','CSSX'):
                    rec['MXQSRQ'] ,rec['MXCJRQ'] ,rec['MXFSRQ'],rec['MXJSRQ'] = qsrq,qsrq,fsrq,qsrq
            records.append(record)
        table.close()
        return records

    def sjsfw_file(self, cjrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['FWSJLB'] in ('11', '13', '21', '22','01'):
                    rec['FWCLRQ'], rec['FWFSRQ'] = cjrq, fsrq
                elif rec['FWSJLB'] in ('04','03'):
                    rec['FWCLRQ'], rec['FWFSRQ'] = self.t5, fsrq
            records.append(record)
        table.close()
        return records

    def dsfmx_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['MXYWLB'] in ('DESY','DCBF'):
                    rec['MXJYRQ'],rec['MXQSRQ'],rec['MXFSRQ'] = self.t,self.t,self.t
            records.append(record)
        table.close()
        return records

    def sisdz_file(self, fsrq=None):
        if fsrq is None:
            fsrq = self.t
        return self.get_data(DZFSRQ=fsrq)

    def zsmx_file(self,fsrq=None):
        if fsrq is None:
            fsrq = self.t #转入后，人工生成申报文件，和正常操作一致
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['MXFSRQ'] = self.replace_time(rec['MXFSRQ'], fsrq)
            records.append(record)
        table.close()
        return records

    def zsmxfk_file(self,  fsrq=None):
        if fsrq is None: #征税明细反馈和征税明细匹配条件是结算账户、结算日期，结算流水号
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['FKFSRQ'] = self.replace_time(rec['FKFSRQ'], fsrq)
            records.append(record)
        table.close()
        return records


    def szhk_sjsjg_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['WTRQ'], rec['QSRQ'], rec['JSRQ'], rec['FSRQ'] = cjrq, qsrq, jsrq, fsrq
                if rec['YWLB'] in ('QPPF'):
                    rec['WTRQ'] = None
                if rec['YWLB'] in ('ZT01', 'ZT02', 'ZT03', 'ZTFY'):
                    rec['JSRQ'] = cjrq
                if rec['YWLB'] in ('QPTG', 'TGZX','TGDJ','SGZX'):
                    rec['WTRQ'], rec['JSRQ'] = None, cjrq
            records.append(record)
        table.close()
        return records

    def szhk_sjsmx1_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        return self.get_data(JYRQ=cjrq, QSRQ=qsrq, JSRQ=jsrq, FSRQ=fsrq)

    def szhk_sjsmx2_file(self, qsrq=None, jsrq=None, fsrq=None):
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['YWLB'] == 'TGZH':
                    rec['QSRQ'] ,rec['JSRQ'] ,rec['FSRQ'] = qsrq,jsrq,fsrq
            records.append(record)
        table.close()
        return records

    def sjsqs_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['QSYWLB'] == 'FJ01':
                    rec['QSCJRQ'] = self.t
                    rec['QSQSRQ'] = self.t
                    rec['QSJSRQ'] = self.t
                    rec['QSFSRQ'] = self.t
            records.append(record)
        table.close()
        return records

    def szhk_sjsqs_file(self, qsrq=None, jsrq=None, fsrq=None):
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['YWLB'] in ('TGZH','QPPF'):
                    rec['QSRQ'] = qsrq
                    rec['JSRQ'] = jsrq
                    rec['FSRQ'] = fsrq
            records.append(record)
        table.close()
        return records

    def szhk_sjszj_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['YWLB'] in ('TGZH'):
                    rec['JZRQ'] = self.t
            records.append(record)
        table.close()
        return records

    def szhk_sjsdz_file(self):
        return self.get_data(FSRQ=self.t)

    def sjsdvpjg_file(self):
        return self.get_data(JGFSRQ=self.t)

    def szhk_tzxx_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['FSRQ'] = self.t
                if rec['TZLB'] in ('H06'):  # h06,投票开始日为前10天，截止日为后10天
                    rec['RQ3'] = OracleDatabase().get_trade_date(10)
                    rec['RQ2'] = OracleDatabase().get_last_trade_date(10)
                    if rec['LX1'] in ('Y'):  # 有登记日是，设置登记日，没有登记日时不处理，
                        rec['RQ2'] = self.lasttradedate1
            records.append(record)
        table.close()
        return records

    def szyh_sjsqs_file(self, qsrq=None, jsrq=None, fsrq=None):
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = OracleDatabase().get_trade_date(1)
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['QSCJRQ'],rec['QSQSRQ'],rec['QSJSRQ'],rec['QSFSRQ'] = qsrq,qsrq,qsrq,qsrq
            records.append(record)
        table.close()
        return records

    def op_ccbd_file(self):
        return self.get_data(BDRQ=self.t)

    def op_bzjmx_file(self):
        return self.get_data()

    def op_bzjzh_file(self):
        return self.get_data()

    def op_hycc_file(self):
        return self.get_data()

    def tzxx_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['TZRQ'] = self.t
                if rec['TZLB'] in ('006','041'):
                    rec['RQ1'] = self.t
                elif rec['TZLB'] in ('020','030','050'):
                    rec['RQ1'],rec['RQ2'] = self.t5,self.lasttradedate1
            records.append(record)
        table.close()
        return records

    def op_tzxx_file(self):
        return self.get_data(TZRQ=self.t, RQ1=self.t)

    def op_zhccmx_file(self):
        return self.get_data()

    def op_jsmx_file(self, cjrq=None, jsrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['YWLX'] in ('13', 'Q02'):
                    rec['JYRQ'] = cjrq
                    rec['QSRQ'] = fsrq
                    rec['JSRQ'] = jsrq
                else:
                    rec['JYRQ'] = cjrq
                    rec['QSRQ'] = cjrq
                    rec['JSRQ'] = cjrq
            records.append(record)
        table.close()
        return records

    def sjsmx1_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        return self.get_data(MXCJRQ=cjrq, MXQSRQ=qsrq, MXJSRQ=jsrq, MXFSRQ=fsrq)

    def sq_jsmx_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(CJRQ=cjrq, QSRQ=cjrq, JSRQ=cjrq, FSRQ=cjrq)

    def sq_hycb_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(BDRQ=cjrq)

    def sq_hycc_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(FSRQ=cjrq)

    def sq_bzjmx_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(FSRQ=cjrq)

    def sq_zqje_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        return self.get_data(QSRQ=cjrq, JSRQ=cjrq, FSRQ=cjrq)

    def bjsjg_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['JGYWLB'].strip() in ('36', '37', 'DZ', '24', '20','30','31','35'): #有部分类别读文件后，类型后有空格，需去空格后判断
                    rec['JGCJRQ'] = self.replace_time(rec['JGCJRQ'], cjrq)
                    rec['JGQSRQ'] = self.replace_time(rec['JGQSRQ'], qsrq)
                    rec['JGJSRQ'] = self.replace_time(rec['JGJSRQ'], jsrq)
                    rec['JGFSRQ'] = self.replace_time(rec['JGFSRQ'], fsrq)
                elif rec['JGYWLB'].strip() in ('B7', 'B5', 'BA', 'B6','BC','BD','7K','7L','7B','DJ','B2'):
                    rec['JGCJRQ'] = self.replace_time(rec['JGCJRQ'], cjrq)
                    rec['JGFSRQ'] = self.replace_time(rec['JGFSRQ'], fsrq)
                elif rec['JGYWLB'].strip() in ('41', '40', 'ZG', '67', '66', '68', '69', '03'):
                    rec['JGCJRQ'] = self.replace_time(rec['JGCJRQ'], cjrq)
                    rec['JGQSRQ'] = self.replace_time(rec['JGQSRQ'], qsrq)
                    rec['JGJSRQ'] = self.replace_time(rec['JGJSRQ'], cjrq)
                    rec['JGFSRQ'] = self.replace_time(rec['JGFSRQ'], fsrq)
            records.append(record)
        table.close()
        return records

    def bjsmx_file(self, cjrq=None, qsrq=None, jsrq=None, fsrq=None):
        if cjrq is None:
            cjrq = self.t
        if qsrq is None:
            qsrq = self.t
        if jsrq is None:
            jsrq = self.t1
        if fsrq is None:
            fsrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['MXYWLB'] in ('00',):
                    rec['MXCJRQ'] = self.replace_time(rec['MXCJRQ'], cjrq)
                    rec['MXQSRQ'] = self.replace_time(rec['MXQSRQ'], qsrq)
                    rec['MXJSRQ'] = self.replace_time(rec['MXJSRQ'], jsrq)
                    rec['MXFSRQ'] = self.replace_time(rec['MXFSRQ'], fsrq)
            records.append(record)
        table.close()
        return records

    def bjstj_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['TJCJRQ'] = self.replace_time(rec['TJCJRQ'], cjrq)
            records.append(record)
        table.close()
        return records

    def bjszj_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['ZJJZRQ'] = self.replace_time(rec['ZJJZRQ'], self.t)
            records.append(record)
        table.close()
        return records

    def bjsdz_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['DZFSRQ'] = self.replace_time(rec['DZFSRQ'], cjrq)
            records.append(record)
        table.close()
        return records

    def bjsgb_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['GBLB'] == 'ZY':
                    rec['GBRQ'] = self.replace_time(rec['GBRQ'], self.t)
                elif rec['GBLB'] == 'QP':
                    rec['GBRQ'] = self.replace_time(rec['GBRQ'], self.t)
                    rec['GBRQ1'] = self.replace_time(rec['GBRQ'], self.t)
            records.append(record)
        table.close()
        return records

    def bjsds_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['BJSCJRQ'] = self.replace_time(rec['BJSCJRQ'], cjrq)
                rec['BJSFSRQ'] = self.replace_time(rec['BJSFSRQ'], cjrq)
            records.append(record)
        table.close()
        return records

    def bjsgb_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['GBRQ'] = self.replace_time(rec['GBRQ'], cjrq)
                if rec['GBLB'] == 'QP':
                    rec['GBRQ1'] = self.replace_time(rec['GBRQ1'], cjrq)
            records.append(record)
        table.close()
        return records


    def bjsfw_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['FWCLRQ'] = self.replace_time(rec['FWCLRQ'], cjrq)
                rec['FWFSRQ'] = self.replace_time(rec['FWCLRQ'], cjrq)
                if rec['FWSJLB'] == '03':
                    rec['FWCLRQ'] = self.replace_time(rec['FWCLRQ'], self.t5)
            records.append(record)
        table.close()
        return records


    def bjgzj_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['ZJJZRQ'] = self.replace_time(rec['ZJJZRQ'], cjrq)
            records.append(record)
        table.close()
        return records

    def sjsdz_file(self, fsrq=None):
        if fsrq is None:
            fsrq = self.t
        return self.get_data(DZFSRQ=fsrq)

    def hk_jsmx_file(self):
        return self.get_data(JYRQ=self.t, QSRQ=self.t, JSRQ=self.t2)

    def hk_zqbd_file(self):
        return self.get_data(JYRQ=self.t, FSRQ=self.t)

    def hk_zqye_file(self):
        return self.get_data(JZRQ=self.t)

    def hk_tzxx_file(self):
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                rec['TZRQ'] = self.t
                if rec['TZLB'] in ('H06'): #h06,投票开始日为前10天，截止日为后10天
                    rec['RQ3'] = OracleDatabase().get_trade_date(10)
                    rec['RQ2'] = OracleDatabase().get_last_trade_date(10)
                    print(rec['LX1'])
                    if rec['LX1']  in ('Y'): #有登记日是，设置登记日，没有登记日时不处理，
                        rec['RQ2'] = self.lasttradedate1
            records.append(record)
        table.close()
        return records

    def bc1_file(self):
        return self.get_data(TRADE_DATE=self.t, SETTLEDATE=self.t2)

    def bc9_file(self):
        # YWLX = B2H
        return self.get_data(JYRQ=self.t, QSRQ=self.t, JSRQ=self.t2)

    def bd202_file(self):
        return self.get_data(TRADE_DATE=self.t, SETTLE_DAT=self.t2)

    def bd502_file(self):
        return self.get_data(CHGDATE=self.t)

    def sjsfx_file(self):
        return self.get_data(FXFSRQ=self.t)

    def sjsfx_fxa_file(self):
        return self.get_data(FXFSRQ=self.t)

    def hstgdz_file(self):
        return self.get_data(SXRQ=self.t)

    def khtj_file(self):
        return self.get_data(KHRQ=self.t, QSRQ=self.t1)

    def qtsdxgl_file(self):
        return self.get_data(QYRQ=self.t)

    def qtsyxx_file(self):
        return self.get_data(SYSBRQ=self.t)

    def qtzhzl_file(self):
        return self.get_data(KHRQ=self.t)

    def syxx_file(self):
        return self.get_data(SYSBRQ=self.t)

    def xmzh_file(self):
        return self.get_data(SYSBRQ=self.t)

    def ywls_file(self):
        return self.get_data(SQRQ=self.t, YWRQ=self.t)

    def zbzhdy_file(self):
        return self.get_data()

    def zqzhzl_file(self):
        return self.get_data(KHRQ=self.t)

    def cjjydybbqr_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(SBRQ=cjrq,FSRQ =cjrq)

    #转融通新合约信息
    def zrtxhyxx_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                QX = rec['QX']
                rec['QSRQ'],rec['CJRQ'],rec['HYDQR'] = cjrq,cjrq,OracleDatabase().get_trade_date(QX)
            records.append(record)
        table.close()
        return records

    #转融通合约对账
    def zrthydz_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                QX = rec['QX']
                rec['QSRQ'],rec['CJRQ'],rec['LLDQR'],rec['HYDQR'] = cjrq,cjrq,OracleDatabase().get_trade_date(QX),\
                                                                    OracleDatabase().get_trade_date(QX)
            records.append(record)
        table.close()
        return records


    #转融通T+1日交收通知
    def zrtjstz_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['ZQDM'].strip()  in ('304001',):
                    rec['QSRQ'],rec['CJRQ'],rec['JSRQ'] = cjrq,cjrq,self.t1
                elif rec['HYBH'] == '2021032700000006':
                    rec['QSRQ'], rec['CJRQ'], rec['JSRQ'] = cjrq, cjrq, self.t1

            records.append(record)
        table.close()
        return records


    def fi_jsmx_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['YWLX'] in('701','702','703'):
                    rec['QSRQ'],rec['JYRQ'],rec['JSRQ'] = cjrq,cjrq,cjrq
                elif rec['YWLX'] in('704',):
                    rec['QSRQ'], rec['JSRQ'] = cjrq, cjrq
            records.append(record)
        table.close()
        return records

    def fi_tzxx_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            with record as rec:
                if rec['TZLB'] == '009':
                    rec['TZRQ'],rec['RQ1'] = cjrq,cjrq
                elif rec['TZLB'] in('010',):
                    rec['TZRQ'], rec['RQ1'] = cjrq, self.lasttradedate1
            records.append(record)
        table.close()
        return records

    def fi_zqbd_file(self, cjrq=None):
        """
        修改成交日期，获取修改日期后的dbf文件数据列表
        :param cjrq:
        :return:
        """
        if cjrq is None:
            cjrq = self.t
        return self.get_data(BDRQ=cjrq)

    def fi_zqye_file(self, cjrq=None):
        if cjrq is None:
            cjrq = self.t
        records = []
        table = self.dbf_file.open(mode=dbf.READ_WRITE)
        for record in table:
            records.append(record)
        table.close()
        return records


def creat_new_dbf(path):
    """
    传路径，操作路径下所有dbf文件，修改日期并放至当前交易日期目录下
    :param path:
    :return:
    """
    dbf_names = BaseAction().get_dbf(path)
    dbf_result = []
    if not dbf_names:
        logger().error('当前路径下未找到dbf文件{}'.format(path))
        dbf_result.append('当前路径下未找到dbf文件{}'.format(path))
        return dbf_result
    for dbf_file in dbf_names:
        dbf_file_path = os.path.join(path, dbf_file)
        new_init = DbfOperation(dbf_file_path)
        func_name = dbf_file.replace('.dbf', '') + '_file'
        if hasattr(new_init, func_name):  # 判断方法是否存在
            new_dbf = getattr(new_init, func_name)
            new_dbf_result = new_init.creat_dbf(new_dbf(), dbf_file.replace('.dbf', ''))
            if new_dbf_result is False:
                dbf_result.append('{}创建失败'.format(dbf_file))
        else:
            logger().error('{} 未找到对应方法，请补充'.format(dbf_file))
            dbf_result.append('{} 未找到对应方法，请补充'.format(dbf_file))
    return dbf_result


if __name__ == '__main__':
    dbf_file = DbfOperation(r'D:\sjsfx.dbf')
    dbf_file.delete_record()
