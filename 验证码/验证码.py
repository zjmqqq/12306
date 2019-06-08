# coding=utf-8

import os

import requests


# 下载验证码图片
def save_image():
    image_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.7519806101835129'
    response = session.get(image_url)
    if not os.path.exists('image'):
        os.mkdir('image')
    file_path = 'image/1.jpg'
    with open(file_path, 'wb') as f:
        f.write(response.content)


# 校正验证码
def check_captcha():
    check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    data = {
        'answer': get_answer(input("请输入正确验证码的序号>>>:")),  # 正确图片的像素
        'login_site': 'E',
        'rand': 'sjrand'
    }
    response = session.post(check_captcha_url, data=data)
    print(response.text)


# 手动输入验证码序号
def get_answer(index):
    point = {
        '1': '37,46',
        '2': '111,46',
        '3': '181,46',
        '4': '254,46',
        '5': '37,116',
        '6': '111,116',
        '7': '181,116',
        '8': '254,116'
    }
    index = index.split(',')
    temp = []
    for item in index:
        temp.append(point[item])
    return ','.join(temp);


# 校验用户名和密码
def check_username_paasword():
    save_image()
    check_captcha()
    check_username_password_url = 'https://kyfw.12306.cn/passport/web/login'
    data = {
        'appid': 'otn',
        'password': 'wyd206020',  # 帐号密码故意写错
        'username': '2414615579@qq.com'
    }
    response = session.post(check_username_password_url, data=data)
    print(response.text)


session = requests.Session()  # 创建一个session对象,实现自动会话处理
login_url = 'https://kyfw.12306.cn/otn/login/init'  # 登录页面,获取cookie
session.get(login_url)
check_username_paasword()
