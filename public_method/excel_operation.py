import os
import pandas as pd
from xlrd import open_workbook
# xlrd更新到了2.0.1版本，只支持.xls文件，不支持.xlsx文件.所以当运行pandas.read_excel(‘xxx.xlsx’)会报错。可以安装旧版xlrd.
# 在cmd中运行     pip install xlrd==1.2.0
from log.logger import logger


class SheetTypeError(Exception):
    '''
    excle的sheet不是数字或名称时，抛错
    '''
    pass

class ExcelOperation:


    def __init__(self, excel_path):
    # 初始化Excel，传入xlsx文件路径
        if os.path.exists(excel_path):
            self.excel = excel_path
        else:
            raise FileNotFoundError('文件不存在！')

    def read_excel(self,sheet, return_dict = True):
        '''
        读取Excel，传入sheet表名，或者需要读取的sheet表位置，return_dict控制数据返回格式
        :param sheet:传入sheet表名
        :param return_dict:控制数据返回格式
        :return:
        '''
        if type(sheet) == int:
            data = self.openwork_index(sheet)
        elif type(sheet) == str:
            data = self.openwork_name(sheet)
        else:
            logger().error('sheet参数错误')
            return False
        if return_dict:
            data_list = []
            for s in range(1,len(data)):
                data_list.append(dict(zip(data[0],data[s])))
            logger().info(data_list)
            return data_list
        else:
            logger().info(data)
            return data


    def openwork_index(self,sheet:int):
        '''
        通过sheet位置获取数据，返回列表
        :param sheet:
        :return:
        '''
        logger().info('打开Excel：{}，获取 位置 {} 表信息'.format(self.excel, sheet))
        workbook = open_workbook(self.excel)
        if sheet >= self.get_sheet_number():
            logger().error('sheet表参数错误,可接受最大参数：{}，传参：{}'.format(self.get_sheet_number()-1,sheet))
            return False
        try:
            data = []
            s = workbook.sheet_by_index(sheet)
            for i in range(s.nrows):
                data.append(s.row_values(i))
            return data
        except Exception as e:
            logger().error('获取sheet表数据错误')
            logger().error(e)
            return False

    def openwork_name(self,sheet:str):
        '''
        通过sheet名称获取数据，返回列表
        :param sheet:
        :return:
        '''
        sheet = sheet.replace(' ','').lower()
        logger().info('打开Excel：{}，获取 名称 {} 表信息'.format(self.excel, sheet))
        sheet_names = self.get_sheet_names()
        workbook = open_workbook(self.excel)
        # if sheet not in self.get_sheet_names():
        #     logger().error('sheet表名称,可接受参数：{}，传参：{}'.format(self.get_sheet_names(), sheet))
        #     return False

        data = []
        for sheet_name in sheet_names:
            if sheet_name.replace(' ','').lower() == sheet:
                s = workbook.sheet_by_name(sheet_name)
                for i in range(s.nrows):
                    data.append(s.row_values(i))
                return data
        logger().error('sheet表不存在：{}'.format(sheet))
        return False


    def get_sheet_names(self):
        '''
        获取sheet表名称
        :return:
        '''
        # xlsx = pd.read_excel(self.excel)
        # return list(xlsx.keys())
        xlsx = pd.ExcelFile(self.excel)
        return xlsx.sheet_names
    def get_sheet_number(self):
        '''
        获取sheet表个数
        :return:
        '''
        return len(self.get_sheet_names())



if __name__ == '__main__':
    e = r'C:\Users\admin\Desktop\日终通用数据.xlsx'
    # data = pd.read_excel(e)
    # print(list(data.keys()))
    data = ExcelOperation(e).read_excel('UnifiedInFileData') #UnifiedInFileData
    # for i in data:
    #     print(i)