from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import base64
import re
import time
from bs4 import BeautifulSoup


class Demo():
    def __init__(self):
        self.coordinate = [[-105, -20], [-35, -20], [40, -20], [110, -20], [-105, 50], [-35, 50], [40, 50], [110, 50]]

    def login(self):
        login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(
            'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_window_size(1200, 900)
        driver.get(login_url)
        account = driver.find_element_by_class_name("login-hd-account")
        account.click()
        time.sleep(3)
        userName = driver.find_element_by_id("J-userName")
        userName.send_keys("###")
        time.sleep(3)
        password = driver.find_element_by_id("J-password")
        password.send_keys("###")
        self.driver = driver

    def getVerifyImage(self):
        try:

            img_element = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "J-loginImg"))
            )

        except Exception as e:
            print(u"网络开小差,请稍后尝试")
        base64_str = img_element.get_attribute("src").split(",")[-1]
        imgdata = base64.b64decode(base64_str)
        with open('verify.jpg', 'wb') as file:
            file.write(imgdata)
        self.img_element = img_element

    def getVerifyResult(self):
        url = "http://littlebigluo.qicp.net:47720/"
        files = {'pic_xxfile': open("verify.jpg", 'rb')}
        response = requests.request("POST", url, data={"type": "1"}, files=files)
        result = []
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in (soup.find('p').find('font').find('font').find('b').text.split(" ")):
            result.append(int(i) - 1)
        self.result = result
        print(result)

    def moveAndClick(self):
        try:
            Action = ActionChains(self.driver)
            for i in self.result:
                Action.move_to_element(self.img_element).move_by_offset(self.coordinate[i][0],
                                                                        self.coordinate[i][1]).click()
            Action.perform()
        except Exception as e:
            print(e.message())

    def submit(self):
        self.driver.find_element_by_id("J-login").click()

    def __call__(self):
        self.login()
        time.sleep(3)
        self.getVerifyImage()
        time.sleep(1)
        self.getVerifyResult()
        time.sleep(1)
        self.moveAndClick()
        time.sleep(1)
        self.submit()
        time.sleep(1)

if __name__=="__main__":
    demo=Demo()
    demo.__call__()
