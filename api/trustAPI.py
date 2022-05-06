import app


class TrustAPI:
    def __init__(self):
        self.trust_url = app.BASE_URL + '/trust/trust/register'
        self.recharge_verify_code_url = app.BASE_URL + '/common/public/verifycode/'
        self.get_recharge_url = app.BASE_URL + '/trust/trust/recharge'

    # 开户申请
    def trust_requests(self, session):
        response = session.post(self.trust_url)
        return response

    # 获取充值验证码
    def get_recharge_verify_code(self, session, r):
        url = self.recharge_verify_code_url + r
        response = session.get(url)
        return response

    # 调取第三方接口请求，充值成功
    def get_recharge(self, session, paymentType="chinapnrTrust", amount="", formStr="reForm", valicode="8888"):
        data = {
            "paymentType": paymentType,  # 默认充值类型
            "amount": amount,  # 充值金额
            "formStr": formStr,  # 默认格式
            "valicode": valicode
        }
        response = session.post(self.get_recharge_url, data=data)
        return response
