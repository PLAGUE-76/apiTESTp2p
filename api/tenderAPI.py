import app


class tenderAPI:
    def __init__(self):
        self.get_tender_url = app.BASE_URL + '/common/loan/loaninfo'
        self.risk_appraisal_url = app.BASE_URL + '/risk/answer/submit'
        self.tender_url = app.BASE_URL + '/trust/trust/tender'

    # 获取
    def get_tender(self, session, id):
        data = {"id": id}
        response = session.post(self.get_tender_url, data)

        return response

    def risk_appraisal(self, session, answer1="B", answer2="B", answer3="B", answer4="B", answer5="B", answer6="B",
                       answer7="B", answer8="B", answer9="B", answer10="B"):
        data = {
            "answers_1": answer1,
            "answers_2": answer2,
            "answers_3": answer3,
            "answers_4": answer4,
            "answers_5": answer5,
            "answers_6": answer6,
            "answers_7": answer7,
            "answers_8": answer8,
            "answers_9": answer9,
            "answers_10": answer10,
        }
        response = session.post(self.risk_appraisal_url, data=data)
        return response

    def tender(self, session, id, depositCertificate="-1", amount="1000", pwd=app.tender_pwd):
        data = {
            "id": id,
            "depositCertificate": depositCertificate,
            "amount": amount,
            "password": pwd

        }
        response = session.post(self.tender_url, data)

        return response
