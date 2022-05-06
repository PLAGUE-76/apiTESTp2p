import logging
import unittest, app, requests
from utils import assert_utils, soup_third_api

from api.login_api import login_api
from api.tenderAPI import tenderAPI


class tender(unittest.TestCase):
    def setUp(self) -> None:
        self.login = login_api()
        self.Tender = tenderAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 认证成功
    def test001_risk_appraisal_succeed(self):
        response = self.login.user_login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login response{}".format(response.json()))
        response = self.Tender.risk_appraisal(self.session)
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual("提交成功", response.json().get("data"))
        logging.info("risk_appraisal response{}".format(response.json()))

    # 认证错误
    def test002_risk_appraisal_Wrong_answer(self):
        response = self.login.user_login(self.session, phone=app.phone4)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login response{}".format(response.json()))
        response = self.Tender.risk_appraisal(self.session, answer4="error")
        self.assertEqual(200, response.status_code)
        self.assertIn("error", response.json().get("data"))
        logging.info("risk_appraisal response{}".format(response.json()))

    # 获取投资页详情
    def test003_get_tender_msg(self):
        response = self.login.user_login(self.session, phone=app.phone4)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login response{}".format(response.json()))
        response = self.Tender.get_tender(self.session, "702")
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertIn("702", response.json().get("data").get("loan_info").get("id"))
        logging.info("get_tender response{}".format(response.json()))

    # 投资转第三方成功
    def test004_tender_succeed(self):
        response = self.login.user_login(self.session, phone=app.phone1)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login response{}".format(response.json()))
        response = self.Tender.tender(self.session, app.tb_id)  # 投资申请
        self.assertEqual(200, response.status_code)
        logging.info("tender response{}".format(response.text))
        print(response.json())
        from_data = response.json().get("description").get("form")
        logging.info("from_data response= {}".format(response.json()))
        response = soup_third_api(from_data)  # 第三方跳转申请
        logging.info("thirdAPI response= {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertIn('InitiativeTender OK', response.text)
