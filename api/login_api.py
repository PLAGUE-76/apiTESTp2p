import app


class login_api:
    def __init__(self):
        self.getImgCode_url = app.BASE_URL + '/common/public/verifycode1/'
        self.getSmsCode_url = app.BASE_URL + '/member/public/sendSms'
        self.add_user_url = app.BASE_URL + '/member/public/reg'
        self.user_login_url = app.BASE_URL + '/member/public/login'

    def get_ImgCode(self, session, r):
        url = self.getImgCode_url + r
        response = session.get(url)
        return response

    def get_SmsCode(self, session, phone, ImgCode='8888'):
        url = self.getSmsCode_url
        data = {
            "phone": phone,
            "imgVerifyCode": ImgCode,
            "type": "reg"
        }
        response = session.post(url, data=data)
        return response

    def add_user(self, session, phone, pwd=app.pwd, ImgCode=app.imgCode, smsCode=app.smsCode, invite_phone="",
                 dy_server="on"):
        url = self.add_user_url
        data = {
            "phone": phone,
            "password": pwd,
            "verifycode": ImgCode,
            "phone_code": smsCode,
            "invite_phone": invite_phone,
            "dy_server": dy_server
        }
        response = session.post(url, data=data)
        return response

    def user_login(self, session, phone=app.phone1, pwd=app.pwd):
        url = self.user_login_url
        data = {
            "keywords": phone,
            "password": pwd,
        }
        response = session.post(url, data=data)
        return response
