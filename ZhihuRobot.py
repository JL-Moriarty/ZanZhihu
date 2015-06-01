__author__ = 'Wang'
#encoding:utf-8

'''
知乎机器人
'''

import sys
import requests
from BeautifulSoup import BeautifulSoup

class ZhihuRobot:

    # 构造函数 初始化用户名密码
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        s = requests.session()
        _xsrf = BeautifulSoup(s.get('http://www.zhihu.com/').content).find(type='hidden')['value']
        data = {
            "_xsrf": _xsrf,
            "email": self.username,
            "password": self.password,
            "remember": "y"
        }
        header = {
            #"Accept": "\"*/*\"",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        cookie = dict(
            _alicdn_tc2="AQAAAA6A9WSFIwEAk97KAb/853fo9A2r",
            #_alicdn_tc2="AQAAAC6iPgOPLAAAk97KAaLTyxGHE6Qt",
            #_alicdn_tc2="AQAAAGNi8yTmaQMAk97KAZYIKdMiHNwh",
            #_alicdn_tc2="AQAAAKjzPixX5w4Ak97KAXOW9SDbFWEj",
            z_c0="\"QUJCQ0VVSFpLd2dYQUFBQVlRSlZUZnJlazFVWmppeFBYeDVKOUtDa3otamtpZlFKb0pTR0VnPT0="
                 "|1433162234|3bd3b970f08854b13e607527febe0c5004ad7a31\""
        )
        try:
            r_login = s.post("http://www.zhihu.com/login", data=data, cookie=cookie)
            print(r_login.text)
        except Exception as e:
            print("login error")
            sys.exit(-1)
        return

    # 点赞
    def zan(self):
        return

if __name__ == '__main__':
    robot = ZhihuRobot('weimw0417@163.com', 'admin123456')
    robot.login()


