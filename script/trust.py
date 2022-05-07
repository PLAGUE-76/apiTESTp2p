import logging, unittest, requests
import random

from api.login_api import login_api
from api.trustAPI import TrustAPI
from utils import assert_utils, soup_third_api


class trust_test(unittest.TestCase):
    r = random.random()

    def setUp(self) -> None:
        self.login = login_api()
        self.trust = TrustAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 开户申请
    def test001trust(self):
        response = self.login.user_login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.trust.trust_requests(self.session)  # 开户调取第三方请求
        logging.info("trust response= {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        from_data = response.json().get("description").get("form")
        logging.info("from_data response= {}".format(response.json()))
        response = soup_third_api(from_data)
        logging.info("thirdAPI response= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertIn('UserRegister OK', response.text)

    # 获取充值验证码
    def test002_recharge_verify_code(self):
        response = self.login.user_login(self.session)
        # logging.info("login response= {}".format(response.text))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.trust.get_recharge_verify_code(self.session, str(self.r))
        logging.info("recharge_verify_code= {}".format(response.text))
        self.assertEqual(200, response.status_code)

    # 验证码错误，获取充值信息失败
    def test003_get_recharge_msg(self):
        response = self.login.user_login(self.session)
        logging.info("login response= {}".format(response.text))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.trust.get_recharge_verify_code(self.session, str(self.r))
        # logging.info("recharge_verify_code= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        response = self.trust.get_recharge(self.session, amount="100000", valicode="9998")
        logging.info("get_recharge= {}".format(response.text))
        assert_utils(self, response, 200, 100, "验证码错误")

    # 调取第三方接口请求，充值成功
    def test004_recharge(self):
        response = self.login.user_login(self.session)
        # logging.info("login response= {}".format(response.text))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.trust.get_recharge_verify_code(self.session, str(self.r))
        # logging.info("recharge_verify_code= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        response = self.trust.get_recharge(self.session, amount="100000")
        from_data = response.json().get("description").get("form")
        logging.info("from_data response= {}".format(response.json()))
        response = soup_third_api(from_data)
        logging.info("thirdAPI response= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertIn('NetSave OK', response.text)
