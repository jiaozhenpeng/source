import logging
import os
from datetime import datetime

from config import  PathConfig


class logger(object):
    '''
        使用logger.info('日志内容打印日志')
    '''

    def __init__(self, logger_name='name'):
        self.logger = logging.getLogger(logger_name)  # 创建日志收集器
        if not self.logger.handlers: # 解决日志重复问题，避免重复创建handler
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
            console_formatter = logging.Formatter('%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
            log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
            if os.path.exists(PathConfig().log()) is False:
                os.mkdir(PathConfig().log())
            file_path = os.path.join(PathConfig().log(),log_filename)
            fileHandler = logging.FileHandler(file_path, encoding='utf-8', mode='a')
            consoleHandler = logging.StreamHandler()
            fileHandler.setLevel(logging.INFO)
            consoleHandler.setLevel(logging.DEBUG)
            fileHandler.setFormatter(formatter)
            consoleHandler.setFormatter(console_formatter)
            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

    def info(self, message):
        self.logger.info(message)

    def de_bug(self,message):
        self.logger.debug(message)

    def error(self,message):
        self.logger.error(message)


if __name__ == '__main__':
    for i in range(4):
        logger().info('测试')
