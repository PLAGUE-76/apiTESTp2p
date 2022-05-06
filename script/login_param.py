from parameterized import parameterized
import logging
import random
import unittest
from time import sleep
import requests
import app
from api.login_api import login_api
from utils import assert_utils, read_param_data, DButils


class login_param(unittest.TestCase):
    r = random.random()

    @classmethod
    def setUpClass(cls) -> None:
        sql1 = "delete from mb_member_register_log where phone in ('13992345679','13822345678','13832345679','13982345679');"
        DButils.delete(app.DB_mem, sql1)
        logging.info("delete sql = {}".format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13992345679','13822345678','13832345679','13982345679');"
        DButils.delete(app.DB_mem, sql2)
        logging.info("delete sq2 = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13992345679','13822345678','13832345679','13982345679');"
        DButils.delete(app.DB_mem, sql3)
        logging.info("delete sq3 = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in ('13992345679','13822345678','13832345679','13982345679');"
        DButils.delete(app.DB_mem, sql4)
        logging.info("delete sq4 = {}".format(sql4))

    def setUp(self):
        self.login_api = login_api()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    # 获取图片验证码
    @parameterized.expand(
        read_param_data('ImgVerify.json', 'test_get_img_code', 'type,status_code'))
    def test001get_img_code(self, type, status_code):
        r = ''
        if type == "float":
            r = str(random.random())
        if type == "int":
            r = str(random.randint(1000, 9999))
        if type == "char":
            r = str("".join(random.sample("asdfsadffdgdfsf", 5)))
        response = self.login_api.get_ImgCode(self.session, r)
        self.assertEqual(status_code, response.status_code)
        logging.info("r = {} get_ImgCode = {}".format(r, response))

    # 获取短信验证码
    @parameterized.expand(
        read_param_data("smsCode.json", "test_get_sms_code", "phone,ImgCode,status_code,status,description"))
    def test002get_sms_code(self, phone, ImgCode, status_code, status, description):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        logging.info("r = {} get_ImgCode = {}".format(self.r, response))
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, phone=phone, ImgCode=ImgCode)  # 才能获取短信
        logging.info("get_SmsCode = {}".format(response.json()))
        assert_utils(self, response, status_code, status, description)

    # 手机号码为空，获取短信验证码失败
    def test003_get_sms_code_Is_smsCode_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, '')  # 才能获取短信
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 不调用图片验证码接口，获取短信验证码失败
    def test004_get_sms_code_Is_smsCode_failed(self):
        response = self.login_api.get_SmsCode(self.session, app.phone1)  # 才能获取短信
        assert_utils(self, response, 200, 100, '图片验证码错误')

    # 用户注册
    @parameterized.expand(read_param_data("register.json", "test_register",
                                          "phone,password,verifycode,phone_code,invite_phone,dy_server,status_code,status,description"))
    def test005_register(self, phone, password, verifycode, phone_code, invite_phone, dy_server, status_code, status,
                         description):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, phone)  # 才能获取短信
        logging.info("get_SmsCode = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, phone=phone, pwd=password, ImgCode=verifycode,
                                           smsCode=phone_code, invite_phone=invite_phone,
                                           dy_server=dy_server)
        logging.info("register = {}".format(response.json()))
        assert_utils(self, response, status_code, status, description)

    # 登录文件名写入
    @parameterized.expand(read_param_data("Login.json", "test_login", "phone,pwd,status_code,status,description"))
    def test006_login(self, phone, pwd, status_code, status, description):
        response = self.login_api.user_login(self.session, phone, pwd)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, status_code, status, description)

    # 密码错误3次，登录失败,锁定状态1分钟后正常登录成功
    def test007_user_login_PwdError_finallyLoginSucceed(self):
        response = self.login_api.user_login(self.session, app.phone1, pwd="123")
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '密码错误1次')
        response = self.login_api.user_login(self.session, app.phone1, pwd="123")
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '密码错误2次')
        response = self.login_api.user_login(self.session, app.phone1, pwd="123")
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录')
        response = self.login_api.user_login(self.session, app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录')
        sleep(60)
        response = self.login_api.user_login(self.session, app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')
