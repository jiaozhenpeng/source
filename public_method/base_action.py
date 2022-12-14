import os
from datetime import datetime

import yaml

from log.logger import logger


class BaseAction():

    def read_yaml(self, path):
        '''
        传yaml文件路径，读取yaml
        :param path:
        :return:
        '''
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                return data
        except Exception as e:
            logger().info('读取yaml文件失败，{}'.format(e))

    def read_sql(self, sql_path):
        '''
        传sql文件路径，将sql添加到列表返回
        :param sql_path:
        :return:
        '''
        list_result = []
        try:
            with open(sql_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    l = line.replace(';', '').replace('\n', '')
                    if l[:6] == 'values':
                        list_result[-1] = list_result[-1] + ' ' + l
                        continue
                    if l != '':
                        list_result.append(l)
            return list_result
        except Exception as e:
            logger().error('SQL文件获取数据出错：{}'.format(e))
        return list_result

    def write_yaml(self, yaml_path, txt_path, key):
        '''
        传入TXT文件路径，写入yaml文件
        :param :
        :return:
        '''
        try:
            list_result = []

            with open(yaml_path, 'a', encoding='utf-8') as f:
                for line in open(txt_path, 'r', encoding='utf-8'):
                    list_result.append(line.replace(';', '').replace('\n', ''))
                yaml.dump({key: list}, f, allow_unicode=True)

        except Exception as e:
            logger().info('读取yaml文件失败，{}'.format(e))

    def get_today_date(self):
        '''
        返回当天日期2022-01-01
        :return:
        '''
        return datetime.now().strftime('%Y-%m-%d')

    def compare_dict(self, dict1, dict2, base_name, *args):
        '''
        对比列表中字典的各项值是否相同，以dict1的键为准，base_name为对比的表，args为不需要对比的键
        dict1 为数据库数据，dict2 为 sheet表数据
        :param dict1:
        :param dict2:
        :param args:
        :return:
        '''
        if dict1 == []:
            return ['数据库：{}未获取到数据'.format(base_name)]
        list_result = []
        key_error = []
        # print(set(args))
        if len(dict1) - len(dict2) != 0:
            list_result.append('表：{}列表中字典数据个数不一致'.format(base_name))
        keys = set(dict1[0].keys()) - set(args)
        for i in range(len(dict1)):
            for key in keys:
                try:
                    dict2[i][key]
                except:
                    continue
                if dict1[i][key] == dict2[i][key]:
                    continue
                elif (dict1[i][key] == '' and dict2[i][key] == None) or (dict1[i][key] == None and dict2[i][key] == ''):
                    continue
                try:
                    float(dict1[i][key])
                    float(dict2[i][key])
                except:
                    error_key = {'key': key, 'value1': dict1[i][key], 'value2': dict2[i][key]}
                    list_result.append('表：{}字典值不一致{}'.format(base_name, error_key))
                    key_error.append('错误字段：{}'.format(key))
                    logger().error(
                        '表：{} 字典值不一致，key：{}，数据库为：{}，sheet表为：{}'.format(base_name, key, dict1[i][key], dict2[i][key]))
                    continue
                if float(dict1[i][key]) - float(dict2[i][key]) == 0:
                    continue
                else:
                    error_key = {'key': key, 'value1': dict1[i][key], 'value2': dict2[i][key]}
                    list_result.append('表：{}字典值不一致{}'.format(base_name, error_key))
                    key_error.append('错误字段：{}'.format(key))
                    logger().error(
                        '表：{}字典值不一致，key：{}，数据库为：{}，sheet表为：{}'.format(base_name, key, dict1[i][key], dict2[i][key]))
        if not list_result:
            logger().info('{}对比无异常'.format(base_name))
        else:
            logger().error('表：{}有异常的key：{}'.format(base_name, list((set(key_error)))))
        return list_result

    def sorted_dict(self, list_data):
        '''
        对列表中的字典进行排序，根据字段 key 的值,条件不满足，暂时不适用
        :param list_data:
        :return:
        '''
        keys = list(list_data[0].keys())
        list_key1, list_key2, list_key3 = keys[0], keys[1], keys[2]
        list_data.sort(key=lambda x: (x[list_key1], x[list_key2], x[list_key3]))
        return list_data

    def stklist_sort(self, list_data):
        '''
        排序stklist表数据根据exchid,regid,stkid,deskid
        :return:
        '''
        list_data.sort(key=lambda x: (x['STKID'], x['DESKID'], x['EXCHID'], x['REGID'],x['STKVALUE'],
                                      x['EXCEPTFROZENQTY'],x['NEWPRICE']))
        return list_data

    def stklistextend_sort(self, list_data):
        '''
        排序stklistextend 表数据
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['STKID'], x['DESKID'], x['EXCHID'], x['REGID'], x['SHAREATTR'], x['CURRENTQTY']))
        return list_data

    def individualdividendtax_sort(self, list_data):
        '''
        排序individualdividendtax 表数据
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['EXCHID'], x['OFFERREGID'], x['KNOCKCODE'], x['DATE2'], x['AMT1']))
        return list_data

    def tradinglog_sort(self, list_data):
        '''
        排序tradinglog表数据，根据briefid,acctid,regid,stkid,reckoningamt
        :param :
        :return:
        '''
        list_data.sort(key=lambda x: ( x['BRIEFID'],x['EXCHID'], x['STKID'], x['REGID'],x['CONTRACTNUM'],x['KNOCKAMT'],
                                       x['RECKONINGAMT'],x['POSTQTY'],x['SHAREATTR'])) #knockqty排序不生效，使用postqty代替
        return list_data

    def tradinglog_sort1(self, list_data):
        '''
        特殊排序tradinglog表数据，增加knockqty后，excel中的数据排序错误，使用这个特殊方法特殊处理，如下
        股转\股份调账
        :param :
        :return:
        '''
        list_data.sort(key=lambda x: ( x['BRIEFID'],x['EXCHID'], x['STKID'], x['REGID'],x['CONTRACTNUM'],
                                       x['RECKONINGAMT']))
        return list_data

    def tradinglog_sort2(self, list_data):
        '''
        特殊排序tradinglog表数据，不加stkid，如下
        深A\信用保护合约\CSSX实物结算
        :param :
        :return:
        '''
        list_data.sort(key=lambda x: ( x['BRIEFID'],x['EXCHID'], x['REGID'],x['CONTRACTNUM'],
                                       x['RECKONINGAMT'],x['KNOCKQTY']))
        return list_data

    def account_sort(self, list_data):
        '''
        排序account表，根据字段currencyid,acctid
        :param :
        :return:
        '''
        list_data.sort(key=lambda x: (x['ACCTID'], x['CURRENCYID'], x['CUSTID'], x['CASHSAVESUM']))
        return list_data

    def openorder_sort(self, list_data):
        """
        排序openorder
        :param list_data:
        :return:
        """
        list_data.sort(key=lambda x: (x['SERIALNUM'], x['ORDERTIME'], x['STKID']))
        return list_data

    def stkauditingerror_sort(self, list_data):
        '''
        排序stkauditingerror表，根据字段STKID,OFFERREGID,EXCHID,BRANCHSTKQTY,EXCHTRUSTEESHIPQTY
        :param list_data:
        :return:
        '''
        list_data.sort(key=lambda x: (
            x['STKID'], x['OFFERREGID'], x['EXCHID'], x['BRANCHSTKQTY'], x['EXCHTRUSTEESHIPQTY'],
            x['SUBSHAREATTR'],x['AUDITINGERRORMSG']))
        return list_data

    def futureposition_sort(self, list_data):
        '''
        排序表futureposition，根据字段['STKID'],['REGID'],['BSFLAG'],['EXCHID'],['PRODUCTCODE']
        :param list_data:
        :return:
        '''
        list_data.sort(key=lambda x: (x['STKID'], x['REGID'], x['BSFLAG'], x['EXCHID'], x['PRODUCTCODE']))
        return list_data

    def iporights_sort(self, list_data):
        '''
        排序表iporights，根据字段['EXCHID'],['OFFERREGID'],['DESKID']
        :param list_data:
        :return:
        '''
        list_data.sort(key=lambda x: (x['EXCHID'], x['OFFERREGID'], x['DESKID']))
        return list_data



    def stkcheckin_sort(self,list_data):
        """
        排序表 stkcheckin
        :param list_data:
        :return:
        """
        list_data.sort(key=lambda x: (x['STKID'],  x['EXCHID'], x['OCCURTIME'], x['RIGHTSSTKID'],x['NETAMT']))
        return list_data

    def exchangerights_sort(self, list_data):
        '''
        排序表 exchangerights
        :param list_data:
        :return:
        '''
        list_data.sort(key=lambda x: (x['STKID'], x['REGID'], x['EXCHID'], x['SERIALNUM'], x['RECKONINGTIME']))
        return list_data

    def futurepositiondetail_sort(self, list_data):
        '''
        futurepositiondetail，根据字段x['STKID'], x['REGID'], x['KNOCKTIME'],x['BSFLAG'], x['EXCHID'], x['KNOCKCODE']
        :param list_data:
        :return:
        :param list_data:
        :return:
        '''
        list_data.sort(key=lambda x: (x['STKID'], x['REGID'], x['KNOCKTIME'], x['BSFLAG'], x['EXCHID'], x['KNOCKCODE']))
        return list_data

    def futuretradinglog_sort(self, list_data):
        '''
        排序futuretradinglog表
        :param list_data:
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['STKID'], x['RECKONINGTIME'], x['SERIALNUM'], x['EXCHID'], x['REGID'], x['KNOCKQTY']))
        return list_data

    def stkoptionsettlement_sort(self, list_data):
        '''
        排序stkoptionsettlement表
        :param list_data:
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['STKID'], x['RECKONINGTIME'], x['SERIALNUM'], x['EXCHID'], x['REGID'], x['KNOCKQTY']))
        return list_data

    def unprocessedreckoningresult_sort(self, list_data):
        '''
        排序unprocessedreckoningresult表
        :param list_data:
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['EXCHID'], x['REGID'],x['STKID'],  x['BRIEFID'], x['CONTRACTNUM'], x['KNOCKCODE'],x['RECKONINGAMT']))
        return list_data

    def unduerepurchasebonds_sort(self, list_data):
        """
        排序 unduerepurchasebonds
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['REGID'], x['CONTRACTNUM'], x['ORDERTIME']))
        return list_data

    def todaytraderslt_sort(self, list_data):
        '''
        排序todaytraderslt表
        :param list_data:
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['KNOCKQTY'], x['KNOCKTIME'], x['KNOCKPRICE']))
        return list_data

    def exchjsmxdetailinfo_sort(self,list_data):
        """
        排序 exchjsmxdetailinfo
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['RECKONINGTIME'], x['SERIALNUM'],x['KNOCKNUM']))
        return list_data

    def finalreckoningresult_sort(self, list_data):
        '''
        排序finalreckoningresult表
        :param list_data:
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['KNOCKQTY'], x['KNOCKTIME'], x['KNOCKPRICE'], x['KNOCKAMT']))
        return list_data

    def unprocessedreckoningresulthis_sort(self, list_data):
        '''
        排序unprocessedreckoningresulthis表
        :param list_data:
        :return:
        '''
        list_data.sort(
            key=lambda x: (x['EXCHID'], x['REGID'],x['STKID'],  x['BRIEFID'], x['CONTRACTNUM'], x['KNOCKCODE'],x['RECKONINGAMT']))
        return list_data

    def quoteRepoPledgeDtl_sort(self, list_data):
        """
        排序 quoteRepoPledgeDtl
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['REGID'], x['KNOCKTIME'], x['CONTRACTNUM']))
        return list_data

    def exchangemessage_sort(self, list_data):
        """
        排序 exchangemessage
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['OCCURTIME'], x['EXCHID'], x['MESSAGETYPE'] ,x['SECURITIESNUM'],x['STKID'],
                           x['MEMO'] ,x['RIGHTSID'] , x['RIGHTSSTKID']))
        return list_data

    def unduerepurchasebondshis_sort(self, list_data):
        """
        排序 unduerepurchasebondshis
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['CONTRACTNUM'], x['ORDERTIME'], x['REGID']))
        return list_data

    def futurecombaction_sort(self, list_data):
        """
        排序 futurecombaction
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['SERIALNUM'], x['CONTRACTNUM'], x['REGID']))
        return list_data

    def regrights_sort(self, list_data):
        """
        排序 regrights
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['REGID'],x['RIGHTSQTY'],x['FROZENQTY'],x['POSTAMT']))
        return list_data

    def futuretraderslt_sort(self, list_data):
        """
        排序 futuretraderslt
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['ORDERID'], x['KNOCKCODE'], x['REGID'], x['FLAG'], x['BSFLAG']))
        return list_data

    def newstkpurchaseinfo_sort(self,list_data):
        """
        排序 newstkpurchaseinfo
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['EXCHID'], x['REGID'],x['ALLOTCOUNT'],x['ALLOTDATE'],x['STKTYPE']))
        return list_data

    def newstkpurchase_sort(self,list_data):
        """
        排序 newstkpurchase
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['STKID'], x['DESKID'],x['CONTRACTNUM']))
        return list_data

    def cf_reckdata_sort(self,list_data):
        """
        排序 cf_reckdata
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['OCCURDATE'], x['SERIALNUM'], x['REGID'],x['STKID'],x['DESKID'],x['EXCHID']))
        return list_data

    def cf_recksum_sort(self,list_data):
        """
        排序 cf_recksum
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['OCCURDATE'], x['BRIEFID'],x['OCCURAMT'],x['DESKID'],x['EXCHID']))
        return list_data

    def cf_reckdetail_sort(self,list_data):
        """
        排序 cf_reckdetail
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['OCCURDATE'], x['RECKONINGTIME'],x['SERIALNUM'],x['BRIEFID'],x['EXCHID']))
        return list_data

    def cf_reckauditing_sort(self,list_data):
        """
        排序 cf_reckauditing
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['OCCURDATE'], x['FORMULAID'],x['FORMULATYPE'],x['AMT1'],x['AMT2'],x['FORMULAID']))
        return list_data

    def virtualregistrationrights_sort(self,list_data):
        """
        排序 cf_reckauditing
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['EXCHID'], x['REGID'],x['STKID'],x['RECKONINGSERIALNUM'],x['MEMO'],x['OCCURQTY']))
        return list_data


    def unifiedinfiledata_sort(self,list_data):
        """
        排序 unifiedinfiledata
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['DBFID'],x['UNIFIEDCODE'],x['REGID'],x['PERSONALID'],x['KNOCKCODE']))
        return list_data

    def CustSellLimitTax_sort(self,list_data):
        """
        排序 CustSellLimitTax
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['DBFID'],x['KNOCKTIME'],x['REGID'],x['CONTRACTNUM'],['KNOCKNUM']))
        return list_data

    def nominalholdingHis_sort(self,list_data):
        """
                排序 NominalholdingHis
                :param list_data:
                :return:
                """
        list_data.sort(
            key=lambda x: (x['ORDERTYPE'], x['REGID'], x['STKID'], x['OCCURQTY']))
        return list_data

    def get_dbf(self, path):
        '''
        传路径，获取当前路径下所有的dbf文件名
        :param path:
        :return:
        '''
        dbf_list = []
        try:
            all_file = os.listdir(path)
            for filename in all_file:
                if '.dbf' in filename.lower():
                    dbf_list.append(filename.lower())
        except Exception as e:
            logger().error('获取dbf文件错误:{}'.format(e))
        return dbf_list

    def stkinfo_sort(self,list_data):
        """
        排序 stkinfo
        :param list_data:
        :return:
        """
        list_data.sort(
            key=lambda x: (x['EXCHID'], x['STKID']))
        return list_data


if __name__ == '__main__':
    print(BaseAction().read_yaml(path=r'../database/oracle_config.yaml'))
    # print('trading' + BaseAction().get_today_date()[:4])
    # print(BaseAction().get_dbf('F:\source\用例数据\深权\普通开仓\准备昨持仓数据'))
    # pass
    # list = BaseAction().read_sql(r'F:\source\用例数据\1.sql')
    # print(list)
    # BaseAction().write_yaml(r'test.yaml', r'F:\source\用例数据\深A\证券转换\stkinfo.sql', 'sql')
