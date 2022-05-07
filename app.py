import logging
import os
import time
from logging import handlers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://user-p2p-test.itheima.net'
phone1 = "13992345679"
phone2 = "13822345678"
phone3 = '13832345679'
phone4 = '13982345679'  # 1-4常规使用
phone5 = '13512345678'  # 已申请借款的手机号码
phone6 = '13822345677'  # 不注册使用的手机号
pwd = "test123456"
imgCode = '8888'
smsCode = "666666"
real_name1 = "窦白亦"
card_id1 = "896311200102129610"
real_name = "潘文杰"
card_id = "328761196807234244"
DB_URL = '121.43.169.97'
DB_user = 'root'
DB_password = 'Itcast_p2p_20191228'
DB_mem = 'czbk_member'
DB_finance = 'czbk_finance'
tender_pwd = '123'
tb_id = 794


def init_log_config():
    logger = logging.getLogger()  # 初始化引入log模块
    logger.setLevel(logging.INFO)  # 设置日志等级 INFO等级所有运行都会记录

    # 创建控制台日志处理器
    sh = logging.StreamHandler()

    logfile = BASE_DIR + "/log/p2p{}.log".format(time.strftime("%y%m%d-%H%M%S"))  # 文件存放位置，和文件名格式，显示日期
    fh = logging.handlers.TimedRotatingFileHandler(logfile, when="M", interval=8, backupCount=3, encoding="utf-8")
    # 格式化器用于处理日志格式
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)  # 格式化器
    # 将格式化器设置到日志处理器里
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 将日志处理器内容输入到LOG文件夹里
    logger.addHandler(sh)
    logger.addHandler(fh)
