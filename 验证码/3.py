import requests
from bs4 import BeautifulSoup
import re
url = "http://littlebigluo.qicp.net:47720/"
files={'pic_xxfile':open("verify.jpg",'rb')}
response = requests.request("POST", url, data={"type": "1"},files=files)
print(response.text)
soup=BeautifulSoup(response.text,"html.parser")
print(soup.find('p').find('font').find('font').find('b').text.split(" "))

