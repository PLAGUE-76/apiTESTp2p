import json
import logging, requests, app

import pymysql
from bs4 import BeautifulSoup


class DButils:
    @classmethod
    def get_conn(cls, db_name):
        conn = pymysql.connect(host=app.DB_URL, user=app.DB_user, password=app.DB_password, database=db_name,
                               autocommit=True)
        return conn

    @classmethod
    def close(cls, cursor=None, conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls, db_name, sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor, conn)


def assert_utils(self, response, status_code, status, desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertIn(desc, response.json().get("description"))


def soup_third_api(from_data):
    # 解析响应内容,并提取内容
    soup = BeautifulSoup(from_data, "html.parser")
    third_url = soup.form["action"]
    logging.info("third_url1= {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    response = requests.post(third_url, data=data)
    return response


# 解析data目录参数化文件
def read_param_data(filename, method_name, param_names):
    # filename： 参数数据文件的文件名
    # method_name: 参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code
    # param_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type,status_code"

    # 获取测试数据文件的文件路径
    file = app.BASE_DIR + "/data/" + filename
    test_case_data = []
    with open(file, encoding="utf-8") as f:
        # 将json字符串转换为字典格式
        file_data = json.load(f)
        # 获取所有的测试数据的列表
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            # 先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in param_names.split(","):
                # 依次获取同一组测试数中每个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            # 每完成一组测试数据的读取，就添加到test_case_data后，直到所有的测试数据读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data

#
# # 解析ImgVerify.json文件
# def read_img_verify_data(file_name):
#     file = app.BASE_DIR + '/data/' + file_name
#     data = []
#     with open(file, encoding="utf-8") as f:
#         verify_data = json.load(f)
#         test_data_list = verify_data.get("test_get_img_code")
#         for test_data in test_data_list:
#             data.append((test_data.get("type"), test_data.get("status_code")))
#
#     return data
#
#
# # 解析短信验证码参数化文件
# def read_sms_code_data(file_name):
#     file = app.BASE_DIR + '/data/' + file_name
#     data = []
#     with open(file, encoding="utf-8") as f:
#         sms_code_data = json.load(f)
#         test_data_list = sms_code_data.get("test_get_sms_code")
#         for test_data in test_data_list:
#             data.append((test_data.get("phone"), test_data.get("ImgCode"),
#                          test_data.get("status_code"), test_data.get("status"), test_data.get("description")))
#     return data
#
#
# # 解析注册参数化文件
# def read_register_data(file_name):
#     file = app.BASE_DIR + '/data/' + file_name
#     data = []
#     with open(file, encoding="utf-8") as f:
#         sms_code_data = json.load(f)
#         test_data_list = sms_code_data.get("test_register")
#         for test_data in test_data_list:
#             data.append((test_data.get("phone"), test_data.get("password"), test_data.get("verifycode"),
#                          test_data.get("phone_code"), test_data.get("invite_phone"), test_data.get("dy_server"),
#                          test_data.get("status_code"), test_data.get("status"), test_data.get("description")))
#     return data
#
#
# # 解析登录参数化文件
# def read_login_data(file_name):
#     file = app.BASE_DIR + '/data/' + file_name  # 定为文件路径
#     data = []  # 空列表装元组数据
#     with open(file, encoding="utf-8")as f:  # 读取该路径文件，写入f
#         login_data = json.load(f)  # 把数据jsom格式拆分
#         login_data_list = login_data.get("test_login")  # 以test_login标题头为json键，读取该键下对应所有数据
#         for login_data in login_data_list:  # 循环读取列表数据到login_data变量里
#             data.append((login_data.get("phone"), login_data.get("pwd"), login_data.get("status_code"),  # 直接把键对应的值加入列表里
#                          login_data.get("status"), login_data.get("description"), login_data.get("dec")))
#     return data  # 列表值返回给函数本身
