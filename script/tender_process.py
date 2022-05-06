import logging
import random
from time import sleep

import app
import utils
from api.login_api import login_api
from api.tenderAPI import tenderAPI
from api.trustAPI import TrustAPI
from api.approve_api import approveAPI
from utils import assert_utils, soup_third_api, DButils
import unittest, requests


class tender_flow(unittest.TestCase):
    r = random.random()

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = login_api()
        cls.tenderAPI = tenderAPI()
        cls.trustAPI = TrustAPI()
        cls.approveAPI = approveAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
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

    # 注册流程
    def test001_register_succeed(self):
        response = self.login_api.get_ImgCode(self.session, str(self.r))  # 获取图片验证码
        logging.info("get_ImgCode{}".format(response.text))
        self.assertEqual(200, response.status_code)
        response = self.login_api.get_SmsCode(self.session, app.phone1)  # 获取短信验证码
        logging.info("get_SmsCode{}".format(response.json()))
        assert_utils(self, response, 200, 200, '短信发送成功')
        response = self.login_api.add_user(self.session, app.phone1)  # 注册用户
        logging.info("register_user{}".format(response.json()))
        assert_utils(self, response, 200, 200, '注册成功')

    # 登录
    def test002_login(self):
        sleep(1)
        response = self.login_api.user_login(self.session)  # 登录
        logging.info("user_login{}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

    # 用户身份证认证，申请开户，风险评估
    def test003_user_approve(self):
        sleep(1)
        response = self.approveAPI.approverealName(self.session, app.real_name, app.card_id)  # 身份证实名认证
        logging.info("approverealName{}".format(response.json()))
        assert_utils(self, response, 200, 200, '提交成功!')
        response = self.trustAPI.trust_requests(self.session)  # 申请开户
        logging.info("trust_requests{}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        from_data = response.json().get("description").get("form")  # 调取响应中的URL
        logging.info("from_data response= {}".format(response.json()))
        response = soup_third_api(from_data)  # 用封装好的函数解析响应内容,并提取内容
        logging.info("third_api_succeed= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertIn('UserRegister OK', response.text)
        response = self.tenderAPI.risk_appraisal(self.session)  # 风险评估
        logging.info("risk_appraisal= {}".format(response.json()))
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual("提交成功", response.json().get("data"))

    # 用户充值
    def test004_user_recharge(self):
        sleep(1)
        response = self.trustAPI.get_recharge_verify_code(self.session, str(self.r))  # 获取充值验证码
        logging.info("third_api_succeed= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        response = self.trustAPI.get_recharge(self.session, amount="100000")  # 充值申请
        logging.info("recharge_requests= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        from_data = response.json().get("description").get("form")  # 第三方充值
        logging.info("recharge_url= {}".format(response.json()))
        response = soup_third_api(from_data)
        logging.info("third_recharge_succeed= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertIn('NetSave OK', response.text)

    # 投资成功
    def test005_tender_succeed(self):
        sleep(1)
        response = self.tenderAPI.tender(self.session, app.tb_id)  # 投资请求
        # logging.info("third_recharge_succeed= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        print(response.json())
        from_data = response.json().get("description").get("form")
        response = soup_third_api(from_data)  # 第三方投资请求
        # logging.info("third_tender_succeed= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertIn('InitiativeTender OK', response.text)
