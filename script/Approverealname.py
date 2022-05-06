import logging
import unittest
import requests
import app
from api.approve_api import approveAPI
from api.login_api import login_api
from utils import assert_utils


class approve(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = login_api()
        self.approveApi = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 姓名身份证正确，实名认证成功
    def test021AppRoveLName(self):
        response = self.login_api.user_login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

        response = self.approveApi.approverealName(self.session, app.real_name1, app.card_id1)
        print(response.json())
        logging.info("approve response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '提交成功!')

    # 姓名为空，实名认证失败
    def test022AppRoveLName(self):
        response = self.login_api.user_login(self.session, phone="13129964788", pwd=app.pwd)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

        response = self.approveApi.approverealName(self.session, real_name="", card_id=app.card_id)
        logging.info("approve response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '姓名未填写')

    # 身份证号为空，实名认证失败
    def test023AppRoveLName(self):
        response = self.login_api.user_login(self.session, phone="13129964789",pwd=app.pwd)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

        response = self.approveApi.approverealName(self.session, app.real_name, card_id="")
        logging.info("approve response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, '请输入身份证号')

    # 获取身份证信息成功
    def test024getAppRoveRealName(self):
        response = self.login_api.user_login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

        response = self.approveApi.getApproverealName(self.session)
        logging.info("approve response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertIn('328****244', response.json().get('card_id'))