import app


class approveAPI:
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.get_approve_url = app.BASE_URL + '/member/member/getapprove'

    # 实名认证
    def approverealName(self, session, real_name, card_id):
        data = {
            "realname": real_name,
            "card_id": card_id
        }
        response = session.post(self.approve_url, data=data, files={'x': 'y'})
        return response

    # 获取认证信息
    def getApproverealName(self, session):
        response = session.post(self.get_approve_url)
        return response
