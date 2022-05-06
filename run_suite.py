import unittest
import app, time
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script.login import login
from script.Approverealname import approve
from script.tender import tender
from script.trust import trust_test
from script.tender_process import tender_flow
from script.login_param import login_param

suite = unittest.TestSuite()  # 初始化测试框架

suite.addTest(unittest.makeSuite(login))  # 登录,注册测试脚本引入
suite.addTest(unittest.makeSuite(approve))  # 身份认证测试脚本引入
suite.addTest(unittest.makeSuite(tender))  # 投资测试脚本引入
suite.addTest(unittest.makeSuite(trust_test))  # 开户，充值测试脚本引入
suite.addTest(unittest.makeSuite(tender_flow))  # 投资流程测试脚本引入
suite.addTest(unittest.makeSuite(login_param))  # 投资流程测试脚本引入

report_file = app.BASE_DIR + '/report/report{}.html' \
    .format(time.strftime("%y%m%d-%H%M%S"))  # 测试报告存放目录，带日期：格式前面小写，后面大写

with open(report_file, 'wb')as f:  # 写入报告
    runner = HTMLTestRunner(f, title='p2p金融项目测试报告', description='test')  # 添加报告的标题
    runner.run(suite)  # 执行测试套件
