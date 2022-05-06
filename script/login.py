import logging
import random
import unittest
from time import sleep

import requests
import app
from api.login_api import login_api
from utils import assert_utils


class login(unittest.TestCase):
    r = random.random()

    def setUp(self):
        self.login_api = login_api()
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    # 获取图片验证码参数为随机小数成功获取
    def test001_get_img_code_random_decimals(self):
        r = random.random()
        response = self.login_api.get_ImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

    # 获取图片验证码参数为随机整数数成功获取
    def test002_get_img_code_random_integer(self):
        r = random.randint(1000, 9999)
        # print(r)
        response = self.login_api.get_ImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

    # 获取图片验证码参数为空获取失败
    def test003_get_img_code_Is_null(self):
        response = self.login_api.get_ImgCode(self.session, '')
        self.assertEqual(404, response.status_code)  # 预期结果404

    # 获取图片验证码参数为字母获取失败
    def test004_get_img_code_letter(self):
        r = "".join(random.sample("abcdefghijklsdjfasdfxcv", 5))
        response = self.login_api.get_ImgCode(self.session, r)
        self.assertEqual(400, response.status_code)

    # 获取短信验证码成功
    def test005_get_sms_code_Is_data_true(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone1)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')

    # 错误图片验证码，获取短信验证码失败
    def test006_get_sms_code_Is_imgCode_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone1, '6666')  # 才能获取短信
        assert_utils(self, response, 200, 100, '图片验证码错误')

    # 图片验证码为空，获取短信验证码失败
    def test007_get_sms_code_Is_imgCode_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone1, '')  # 才能获取短信
        assert_utils(self, response, 200, 100, '图片验证码错误')

    # 手机号码为空，获取短信验证码失败
    def test008_get_sms_code_Is_smsCode_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, '')  # 才能获取短信
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 不调用图片验证码接口，获取短信验证码失败
    def test009_get_sms_code_Is_smsCode_failed(self):
        response = self.login_api.get_SmsCode(self.session, app.phone1)  # 才能获取短信
        assert_utils(self, response, 200, 100, '图片验证码错误')

    # 图片短信验证码正确，注册成功
    def test010_get_imgCode_smsCode_adduser(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone1)  # 才能获取短信
        logging.info("adduser response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone1, invite_phone='')
        logging.info("adduser response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '注册成功')

    # 图片短信验证码正确，输入邀请人，注册成功
    def test011_get_imgCode_smsCode_adduser_invite_phone(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, phone=app.phone1)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, phone=app.phone1, invite_phone="13812345678")
        assert_utils(self, response, 200, 200, '注册成功')

    # 输入数据库内已存在的手机号码，注册失败
    def test012_adduser_invite_phone(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone2)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone2)
        assert_utils(self, response, 200, 100, '手机已存在!')

    # 输入密码为空，注册失败
    def test013_register_pwd_null_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone2)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone2, pwd='')
        assert_utils(self, response, 200, 100, '密码不能为空')

    # 输入图片验证码错误，注册失败
    def test014_register_ErrorPwd_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone2)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone2, ImgCode='9999')
        assert_utils(self, response, 200, 100, '验证码错误')

    # 输入短信验证码错误，注册失败
    def test015_register_ErrorSmsCode_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone2)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone2, smsCode='888888')
        assert_utils(self, response, 200, 100, '验证码错误')

    # 不同意协议，注册失败
    def test016_register_not_dy_server_failed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 先获取验证码
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone2)  # 才能获取短信
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone2, dy_server="off")
        assert_utils(self, response, 200, 100, '验证码错误')

    # 正确账号密码，登录成功
    def test017_user_login_succeed(self):
        response = self.login_api.user_login(self.session, app.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

    # 未注册账号，登录失败
    def test018_user_login_succeed(self):
        response = self.login_api.user_login(self.session, app.phone3)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '用户不存在')

    # 密码为空，登录失败
    def test019_user_login_succeed(self):
        response = self.login_api.user_login(self.session, app.phone1, pwd="")
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '密码不能为空')

    # 密码错误3次，登录失败,锁定状态1分钟后正常登录成功
    def test020_user_login_PwdError_finallyLoginSucceed(self):
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
