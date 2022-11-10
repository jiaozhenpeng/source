import cx_Oracle

from config import PathConfig
from log.logger import logger
from public_method.base_action import BaseAction


class OracleDatabase:

    def __init__(self):
        self.config = BaseAction().read_yaml(path=PathConfig().oracle())
        user = self.config['user']
        password = self.config['password']
        dsn = self.config['dsn']
        self.pool = cx_Oracle.SessionPool(user, password, dsn, min=2, max=5, increment=1, encoding="UTF-8")
        logger().info('初始化数据库成功')

    @staticmethod
    def close_connect(conn, cur):
        """
        关闭数据库链接
        :param conn:
        :param cur:
        :return:
        """
        if cur:
            cur.close()
        if conn:
            conn.close()

    def select_sql(self, *args):
        """
        输入查询语句，返回查询后的结果列表,可查询多条语句
        :param args:
        :return:
        """
        conn = self.pool.acquire()
        cur = conn.cursor()
        list_data = []
        try:
            for s in args:
                logger().info('执行sql：{}'.format(s))
                try:
                    cur.execute(s)
                    rst = cur.fetchall()
                    logger().info('sql执行成功')
                    list_data.append(rst)
                except Exception as e:
                    logger().info('sql执行失败')
                    logger().info(e)
                    return False
            return list_data
        except Exception as e:
            logger().error(e)
            return False
        finally:
            self.close_connect(conn, cur)

    def get_field_name(self, *sql):
        """
        获取查询表的所有字段名
        :param sql:
        :return:
        """
        conn = self.pool.acquire()
        cur = conn.cursor()
        list_data = []
        for s in sql:
            try:
                cur.execute(s)
                rst = [name[0] for name in cur.description]
                logger().info('sql:{} 执行成功,获取表字段名'.format(s))
                list_data.append(rst)
            except Exception as e:
                logger().error('获取字段名错误，错误SQL：{}'.format(s))
                logger().error(e)
        self.close_connect(conn, cur)
        return list_data

    def dict_data(self, sql):
        """
        输入查询语句，获得字典格式数据[{},{}...]
        :param sql:
        :return:
        """
        field_name = self.get_field_name(sql)[0]
        data = self.select_sql(sql)[0]
        list_data = []
        try:
            for s in data:
                list_data.append(dict(zip(field_name, s)))
            logger().info('获取表数据成功')
            logger().info(list_data)
        except Exception as e:
            logger().error('获取表数据失败')
            logger().error(e)
            return False
        return list_data

    def update_sql(self, *args):
        """
        执行修改删除sql操作,可传多个
        :param args:
        :return:
        """
        conn = self.pool.acquire()
        cur = conn.cursor()
        if not args:
            return ['sql数据为空，检查sql文件']
        a = []
        for s in args:
            logger().info('执行sql：{}'.format(s))
            try:
                cur.execute(s)
                logger().info('sql执行成功')
                continue
            except Exception as e:
                logger().error('sql执行失败')
                a.append("{}:执行失败".format(s))
                logger().error(e)
        conn.commit()
        self.close_connect(conn, cur)
        logger().info('sql执行完成')
        return a

    def get_trade_date(self, date=0):
        """
        获取交易日期 T+N 交易日期 返回格式：20220101
        :param date:
        :return:
        """
        conn = self.pool.acquire()
        cur = conn.cursor()
        try:
            sql = self.config['sql']['tradedate']
            trade_date = str(self.select_sql(sql)[0][0][0])[:8]
            for d in range(date):
                new_date = trade_date[6:] + '-' + trade_date[4:6] + '-' + trade_date[:4]
                trade_date = cur.callfunc('getnextsettleday', cx_Oracle.STRING, [new_date, '0'])
                trade_date = trade_date[6:10] + trade_date[3:5] + trade_date[:2]
            logger().info('交易日期获取成功，获取T+{}交易日期:{}'.format(date, trade_date))
            return trade_date
        except Exception as e:
            logger().error('获取交易日期执行失败：{}'.format(e))
        finally:
            self.close_connect(conn, cur)

    def get_last_trade_date(self, date=0):
        """
        获取交易日期 T-N 交易日期 返回格式：20220101
        :param date:
        :return:
        """
        conn = self.pool.acquire()
        cur = conn.cursor()
        try:
            sql = self.config['sql']['tradedate']
            trade_date = str(self.select_sql(sql)[0][0][0])[:8]
            for d in range(date):
                new_date = trade_date[6:] + '-' + trade_date[4:6] + '-' + trade_date[:4]
                trade_date = cur.callfunc('getPrevTradingDay', cx_Oracle.STRING, [new_date, '0'])
                trade_date = trade_date[6:10] + trade_date[3:5] + trade_date[:2]
            logger().info('交易日期获取成功，获取T-{}交易日期:{}'.format(date, trade_date))
            return trade_date
        except Exception as e:
            logger().error('获取交易日期执行失败：{}'.format(e))
        finally:
            self.close_connect(conn, cur)

    def get_new_trade_date(self, data=0):
        """
        获取交易日期，返回格式为 2022-01-01
        :param data:
        :return:
        """
        trade_date = self.get_trade_date(data)
        new_trade_date = trade_date[:4] + '-' + trade_date[4:6] + '-' + trade_date[6:]
        return new_trade_date

    def version_cts(self):
        """
        获取cts版本
        :return:
        """
        try:
            sql = self.config['sql']['version']
            version = self.select_sql(sql)[0][0][0]
            logger().info('版本日期获取成功,当前版本:{}'.format(version))
            return version
        except Exception as e:
            logger().error('版本日期获取失败')
            logger().error(e)
            return False

    def get_last_update(self):
        """
        获取 laststartupdate
        :return:
        """
        try:
            sql = self.config['sql']['laststartupdate']
            last_update = self.select_sql(sql)[0][0][0]
            logger().info('获取 laststartupdate 成功:{}'.format(last_update))
            return str(last_update)
        except Exception as e:
            logger().error('laststartupdate 获取失败')
            logger().error(e)
            return False


if __name__ == '__main__':
    oracle = OracleDatabase()
    sql = "select * from STKLIST where EXCHID = '6' and REGID ='GZ11721600' and STKID ='839106' and DESKID = 'ANQ001'"
    # sql = "SELECT * FROM unprocessedreckoningresult"
    # print(oracle.select_sql(sql))

    # print(oracle.get_field_name(sql)[0])
    print(oracle.dict_data(sql))
    # print(oracle.get_trade_date())
    # print(oracle.version_cts())
    # print(oracle.get_trade_date(1))
    # print(oracle.get_last_update())
