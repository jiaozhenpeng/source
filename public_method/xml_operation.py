import os
from xml.dom.minidom import parse

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction


class XmlOperation(object):
    """
    xml操作
    """

    def __init__(self, path):
        self.path = path

    def creat_path(self, filename):
        """
        新建文件路径
        :param filename: 文件名
        :return:
        """
        dbf_config = BaseAction().read_yaml(path=PathConfig().dbf())
        path = os.path.join(dbf_config['savePath'], OracleDatabase().get_trade_date())
        if os.path.exists(path) is False:
            os.mkdir(path)
            logger().info('创建路径：{}'.format(path))
        file_path = os.path.join(path, filename)
        return file_path

    def fund_reconciliation(self, time=None, filename=None):
        """
        修改资金对账表.xml文件 日期,支持手动输入日期，
        :param time: 日期格式： 20220101
        :return:
        """
        if time is None:
            time = OracleDatabase().get_trade_date()  # 20220101
        if filename is None:
            filename = '资金对账表.xml'
        style_id_s62 = '{}-{}-{}T00:00:00.000'.format(time[:4], time[4:6], time[6:])
        style_id_s64 = '日期：{0}-{0}'.format(time)
        style_id_s67 = time
        # 初始化对象
        DOMTree = parse(self.path)
        # 获取DOMTree中所有的元素
        collection = DOMTree.documentElement
        work_sheet = collection.childNodes[9]
        data = work_sheet.getElementsByTagName("Data")
        # 修改日期
        data[1].childNodes[0].data = style_id_s62
        data[3].childNodes[0].data = style_id_s64
        data[82].childNodes[0].data = style_id_s67
        data[121].childNodes[0].data = style_id_s67
        data[121].childNodes[0].data = style_id_s67
        data[160].childNodes[0].data = style_id_s67
        data[199].childNodes[0].data = style_id_s67
        data[238].childNodes[0].data = style_id_s67
        # 新文件路径
        file_path = self.creat_path(filename)
        fp = open(file_path, 'w', encoding='utf-8')
        # 使用writexml方法将修改后的DOMTree写入到文件。
        DOMTree.writexml(fp, indent='', addindent='', newl='', encoding='utf-8')
        # 写入后关闭文件。
        fp.close()

    def designated_trading(self, time=None, filename=None):
        """
        修改 指定交易日交易所保证金率查询.xml
        :param time:
        :param filename:
        :return:
        """
        if time is None:
            time = OracleDatabase().get_trade_date()  # 20220101
        if filename is None:
            filename = '指定交易日交易所保证金率查询.xml'
        style_id_s62 = '{}年{}月{}日'.format(time[:4], time[4:6], time[6:])
        # 初始化对象
        DOMTree = parse(self.path)
        # 获取DOMTree中所有的元素
        collection = DOMTree.documentElement
        work_sheet = collection.childNodes[7]
        data = work_sheet.getElementsByTagName("Data")
        data[1].childNodes[0].data = style_id_s62
        fp = open(self.creat_path(filename), 'w', encoding='utf-8')
        DOMTree.writexml(fp, encoding='utf-8')
        fp.close()

    def investor_positions(self, time=None, filename=None):
        """
        投资者持仓查询.xml文件
        :param time: 2021
        :param filename: 文件名
        :return:
        """
        if time is None:
            time = OracleDatabase().get_trade_date()  # 20220101
        if filename is None:
            filename = '投资者持仓查询.xml'
        style_id_s62 = '{}年{}月{}日'.format(time[:4], time[4:6], time[6:])
        style_id_s66 = time
        DOMTree = parse(self.path)
        collection = DOMTree.documentElement
        work_sheet = collection.childNodes[9]
        data = work_sheet.getElementsByTagName("Data")
        data[1].childNodes[0].data = style_id_s62
        data[36].childNodes[0].data = style_id_s66
        data[69].childNodes[0].data = style_id_s66
        data[102].childNodes[0].data = style_id_s66
        data[135].childNodes[0].data = style_id_s66
        data[168].childNodes[0].data = style_id_s66
        fp = open(self.creat_path(filename), 'w', encoding='utf-8')
        DOMTree.writexml(fp, encoding='utf-8')
        fp.close()

    def current_exchange(self, time=None, filename=None):
        """
        修改 当前交易所合约手续费率.xml
        :param time:
        :param filename:
        :return:
        """
        if time is None:
            time = OracleDatabase().get_trade_date()  # 20220101
        if filename is None:
            filename = '当前交易所合约手续费率.xml'
        style_id_s62 = '{}年{}月{}日'.format(time[:4], time[4:6], time[6:])
        # 初始化对象
        DOMTree = parse(self.path)
        # 获取DOMTree中所有的元素
        collection = DOMTree.documentElement
        work_sheet = collection.childNodes[7]
        data = work_sheet.getElementsByTagName("Data")
        data[1].childNodes[0].data = style_id_s62
        fp = open(self.creat_path(filename), 'w', encoding='utf-8')
        DOMTree.writexml(fp, encoding='utf-8')
        fp.close()

    def investor_contract(self, time=None, filename=None):
        """
        当前投资者合约手续费率.xml
        :param time:
        :param filename:
        :return:
        """
        if time is None:
            time = OracleDatabase().get_trade_date()  # 20220101
        if filename is None:
            filename = '当前投资者合约手续费率.xml'
        style_id_s62 = '{}年{}月{}日'.format(time[:4], time[4:6], time[6:])
        DOMtree = parse(self.path)
        work_sheet = DOMtree.documentElement.childNodes[7]
        data = work_sheet.getElementsByTagName("Data")
        data[1].childNodes[0].data = style_id_s62
        fp = open(self.creat_path(filename), 'w', encoding='utf-8')
        DOMtree.writexml(fp, encoding='utf-8')
        fp.close()

    def investor_margin(self, time=None, filename=None):
        """
        投资者保证金率.xml
        :param time:
        :param filename:
        :return:
        """
        if time is None:
            time = OracleDatabase().get_trade_date()  # 20220101
        if filename is None:
            filename = '投资者保证金率.xml'
        style_id_s62 = '{}年{}月{}日'.format(time[:4], time[4:6], time[6:])
        DOMtree = parse(self.path)
        work_sheet = DOMtree.documentElement.childNodes[7]
        data = work_sheet.getElementsByTagName("Data")
        data[1].childNodes[0].data = style_id_s62
        fp = open(self.creat_path(filename), 'w', encoding='utf-8')
        DOMtree.writexml(fp, encoding='utf-8')
        fp.close()

    def modify_xml(self, time, filename):
        """
        修改xml文件里面的日期，提前将需要修改的地方做标记,年标记为yyyy,月标记mm，日标记dd
        :param time: 格式 20220101
        :param filename: 文件名
        :return:
        """
        year, month, day = time[:4], time[4:6], time[6:]
        filename = filename + '.xml'
        DOMTree = parse(self.path)
        collection = DOMTree.documentElement
        a = 0
        for i in range(len(collection.childNodes)):
            if 'Worksheet' in str(collection.childNodes[i]):
                a = i
                break
        work_sheet = collection.childNodes[a]
        data = work_sheet.getElementsByTagName("Data")
        for i in range(len(data)):
            try:
                txt = str(data[i].childNodes[0].data)
                new_txt = txt.replace('yyyy', year).replace('mm', month).replace('dd', day)
                if txt != new_txt:
                    data[i].childNodes[0].data = new_txt
                    logger().info('修改前：{}，修改后：{}'.format(txt,new_txt))
            except:
                continue
        fp = open(self.creat_path(filename), 'w', encoding='utf-8')
        DOMTree.writexml(fp, encoding='utf-8')
        fp.close()


if __name__ == '__main__':
    x = XmlOperation(r'F:\自动化\自动化相关\原始数据\xml文件\资金对账表_2019-07-26.xml')
    x.modify_xml('20220101','new')
