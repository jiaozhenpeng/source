import os
import re

from config import PathConfig
from database.oracle_database import OracleDatabase
from log.logger import logger
from public_method.base_action import BaseAction


class TxtOperation():
    """
    txt文本操作
    """

    def __init__(self, txt_path):
        """
        传TXT文本路径，初始化TXT
        :param txt_path:
        """
        self.txt = txt_path

    def get_data(self):
        """
        获取TXT文本数据,根据名称自动修改日期
        :return:
        """
        oracle = OracleDatabase()
        today = oracle.get_trade_date()
        today2 = today[:4] + '-' + today[4:6] + '-' + today[6:]
        txt_file = self.txt.split('\\')[-1].lower().replace('.txt', '')  # 获取文件名
        data_list = []
        # 修改保证金监控中心文件日期
        file_name = (
            'trddata', 'holddata', 'opttrddata', 'optholddata', 'optexerdata', 'custfund', 'otherfund', 'fundchg',
            'delivdetails')
        if txt_file in file_name:
            patten = r'[\d]{4}-[\d]{2}-[\d]{2}'
            # 获取文件中的数据并返回
            with open(self.txt, 'r', encoding='utf-8') as file:
                for record in file:
                    result = re.sub(patten, today2, record)  # 替换日期
                    data_list.append(result)
            logger().info('修改保证金中心文件日期')
            return data_list

        # 修改trns03日期
        elif 'trns03' in txt_file:
            with open(self.txt, 'r', encoding='utf-8') as file:
                for record in file:
                    a = record.split('|')
                    a[10] = today  # trans03第11个字段为日期
                    record = '|'.join(a)
                    data_list.append(record)
            logger().info('修改trns03日期')
            return data_list

        elif txt_file in ('jjgh','zqgh'):
            with open(self.txt, 'r', encoding='utf-8') as file:
                for record in file:
                    a = record.split('|')
                    a[1] = today  # jjgh和zqgh第二个字段为日期
                    record = '|'.join(a)
                    data_list.append(record)
            if txt_file == 'jjgh':
                logger().info('修改jjgh日期')
            elif txt_file == 'zqgh':
                logger().info('修改zqgh日期')
            return data_list



        else:
            logger().error('未匹配到{}文本获取数据的方法'.format(txt_file))
            return False

    def creat_txt(self, filename, list_data=None):
        """
        创建TXT文件，传文件名，保存路径为dbf_config.yaml
        :param filename:
        :param list_data:
        :return:
        """
        if list_data is None:
            list_data = self.get_data()
        filename = filename.lower() + '.txt'
        dbf_config = BaseAction().read_yaml(path=PathConfig().dbf())
        path = os.path.join(dbf_config['savePath'], OracleDatabase().get_trade_date())
        new_path = os.path.join(path, filename)
        # 检查当日清算目录是否存在，如果不存在，创建一个清算目录
        if os.path.exists(path) is False:
            os.mkdir(path)
            logger().info('创建路径：{}'.format(path))
        try:
            with open(new_path, 'a+') as file:
                if os.path.getsize(new_path) > 0:
                    file.write('\n')
                file.writelines(list_data)
                file.flush()
            logger().info('{}文件创建成功'.format(new_path))
        except Exception as e:
            logger().error('{}文件创建失败，错误信息：{}'.format(new_path, e))
            return False


    def replace_txt(self, filename, sourcepath):
        """
        创建TXT文件，传文件名，保存路径为dbf_config.yaml
        文件全文替换日期
        :param filename:
        :param list_data:
        :return:
        """
        dbf_config = BaseAction().read_yaml(path=PathConfig().dbf())
        path = os.path.join(dbf_config['savePath'], OracleDatabase().get_trade_date())
        # 处理源文件路径
        filename = filename.lower() + '.txt'
        new_path = os.path.join(path, filename)
        # 获取交易日期 YYYYMMDD
        today = OracleDatabase().get_trade_date()
        # 检查当日清算目录是否存在，如果不存在，创建一个清算目录
        if os.path.exists(path) is False:
            os.mkdir(path)
            logger().info('创建路径：{}'.format(path))
        try:
            with open(sourcepath, 'r') as file:
                a = file.read()
                final = a.replace('20221125', today)
            with open(new_path, 'w') as f:
                f.write(final)
            logger().info('{}文件创建成功'.format(new_path))
        except Exception as e:
            logger().error('{}文件创建失败，错误信息：{}'.format(new_path, e))
            return False


if __name__ == '__main__':
    txt = TxtOperation(r'F:\source\用例数据\沪A\公司债\公司债现券交易\zqgh.txt')
    print(txt.get_data())
