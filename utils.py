import requests
import time

import jwt
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import re

secret_key = 'ymc1107238486123'


def jwt_encode(json_data):
    token_dict = {
        'iat': time.time(),  # 时间戳
        'exp': time.time() + 30,
    }
    token_dict.update(json_data)
    """payload 中一些固定参数名称的意义, 同时可以在payload中自定义参数"""
    # iss  【issuer】发布者的url地址
    # sub 【subject】该JWT所面向的用户，用于处理特定应用，不是常用的字段
    # aud 【audience】接受者的url地址
    # exp 【expiration】 该jwt销毁的时间；unix时间戳
    # nbf  【not before】 该jwt的使用时间不能早于该时间；unix时间戳
    # iat   【issued at】 该jwt的发布时间；unix 时间戳
    # jti    【JWT ID】 该jwt的唯一ID编号

    # headers
    headers = {
        'alg': "HS256",  # 所使用的加密算法方式
        'kid': "9527",  # key_id
    }

    """headers 中一些固定参数名称的意义"""
    # 调用jwt库,生成json web token
    jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                           secret_key,  # 进行加密签名的密钥
                           algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                           headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                           ).decode('ascii')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
    return jwt_token


def jwt_decode(token):
    try:
        # 需要解析的 jwt        密钥                使用和加密时相同的算法
        data = jwt.decode(token, secret_key, algorithms=['HS256'])
        return data
    except Exception as e:
        # 如果 jwt 被篡改过; 或者算法不正确; 如果设置有效时间, 过了有效期; 或者密钥不相同; 都会抛出相应的异常
        print(e)
        return None



def send_email(receivers, title, msg):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "1836336521@qq.com"  # 用户名
    mail_pass = "tplxonhqdhcsdihb"  # 口令

    message = MIMEText(msg, 'plain', 'utf-8')
    message['Subject'] = Header(title, 'utf-8')
    message['From'] = Header("远通达酒类自营店", 'utf-8')
    message['To'] = Header(receivers[0], 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def validateEmail(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
        # if re.match("/^\w+@[a-z0-9]+\.[a-z]{2,4}$/", email) != None:
        return True
    else:
        return False

if __name__ == '__main__':
    print(jwt_encode({'job_id': '123', 'cost': 1}))
    # print(jwt_decode(
    #     'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ijk1MjcifQ.eyJpYXQiOjE1NzE0MDk0ODIuMzY0MTM2LCJleHAiOjE1NzE0MDk1MTIuMzY0MTM2LCJqb2JfaWQiOiIxMjMiLCJjb3N0IjoxfQ.Sp5OBa_xkZETVgM6rsSOyLw6yql-90ZSWAyUPS50DEg'
    # ))

    res = requests.post(url='http://127.0.0.1:5000/cost_score', json={
        'data': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ijk1MjcifQ.eyJpYXQiOjE1NzE0MTAwMTguMjUzMDYzNywiZXhwIjoxNTcxNDEwMDQ4LjI1MzA2MzcsImpvYl9pZCI6IjEyMyIsImNvc3QiOjF9.KDFTQaguRMO8JC74uUHFFnWPyPYN-0dLqHSdQjk4VZc'})
    print(res.text)
