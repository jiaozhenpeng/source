import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import  PathConfig
from log.logger import logger
from public_method.base_action import BaseAction


class Email:
    def __init__(self):
        config = BaseAction().read_yaml(path=PathConfig().mail())
        self.mail_server = "smtp.163.com"  # 邮箱服务器地址
        self.username_send = config['username_send']  # 邮箱用户名
        self.password = config['password']  # 不是邮箱密码：而是需要使用授权码
        self.username_recv = config['username_recv']  # 收件人，多个收件人用逗号隔开

    def connect_email(self):
        '''
        建立邮箱连接
        :return:
        '''
        try:
            smtp = smtplib.SMTP_SSL(self.mail_server, port=465)  # 邮箱的服务器和端口号
            smtp.login(self.username_send, self.password)  # 登录邮箱
            logger().info('邮件登录成功')
            return smtp
        except Exception as e:
            logger().info('邮箱登录失败，错误信息{}'.format(e))
            return False
    def add_file(self,path):
        '''
        添加附件
        :param path:
        :return:
        '''
        file = MIMEApplication(open(path,'rb').read())
        filename = path.split('\\')[-1]
        file.add_header('Content-Disposition', 'attachment', filename=filename)
        logger().info('添加附件成功-{}'.format(filename))
        return file
    def send_email(self,title,content,file_path = None):
        '''
        :param title:邮件标题
        :param content:邮件内容
        :param file_path: 附件路径
        :return: NONE
        '''
        try:
            smtp = self.connect_email()
            mail = MIMEMultipart('mixed')
            text = MIMEText(content)
            mail.attach(text)
            mail['Subject'] = title
            mail['From'] = self.username_send  # 发件人
            mail['To'] = self.username_recv  # 收件人
            if file_path == None:
                smtp.sendmail(self.username_send, self.username_recv,
                              mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
                smtp.quit()  # 发送完毕后退出smtp
                logger().info('邮件发送成功')
            else:
                file = self.add_file(path=file_path)
                mail.attach(file)
                smtp.sendmail(self.username_send, self.username_recv,
                              mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
                smtp.quit()  # 发送完毕后退出smtp
                logger().info('邮件发送成功')
        except Exception as e:
            logger().info('邮件发送失败，错误信息{}'.format(e))


if __name__ == '__main__':
    Email().send_email('标题','内容', r'F:\创建用户并赋权.txt')