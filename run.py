# test开头的py文件    "./" 为当前文件夹下
# 固定格式，当前文件夹下多个test*.py时不建议使用
import unittest

from database.oracle_database import OracleDatabase
from mail.mail import Email
from test_case.HTMLTestRunner_cn import HTMLTestRunner
import shutil
from database.oracle_database import OracleDatabase



def run_case():
    testCases = unittest.defaultTestLoader.discover(r'F:\source\test_case',pattern='test_*.py')
    # 套件里面添加需要执行的方法 方法需要双引号
    # testSuite.addTest(TestA("test02"))
    # 创建测试套件
    testSuite=unittest.TestSuite()
    # 添加执行的文件
    testSuite.addTest(testCases)

    # 执行套件
    # runner=unittest.TextTestRunner()
    # runner.run(testSuite) # testsuite的运行依赖于TextTestRunner的方法
    # 创建测试运行程序启动器
    version = OracleDatabase().version_cts() # 获取当前CTS版本
    runner = HTMLTestRunner(stream=open(r"F:\source\report\reports.html", "wb"),  # 打开一个报告文件，将句柄传给stream
                            tester='焦振鹏',     # 测试人员姓名
                            verbosity=2,  # 表示测试报告信息的详细程度，一共三个值 默认为1 ，2最详细
                            description="测试版本{}".format(version),  # 报告中显示的描述信息
                            title="自动化测试报告")  # 报告的标题
    runner.run(testSuite)  # 执行测试计划
    #邮箱被限制，暂不发送邮件
    # Email().send_email('清算自动化报告', '清算自动化数据准备完成', r'F:\source\report\reports.html')
    today = OracleDatabase().get_trade_date()
    shutil.copy(r'F:\source\report\reports.html',r'F:\report\prreports{}.html'.format(today))


if __name__ == '__main__':
    run_case()