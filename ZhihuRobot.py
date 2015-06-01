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
        self.s = requests.session()
        self._xsrf = BeautifulSoup(self.s.get('http://www.zhihu.com/').content).find(type='hidden')['value']

    # 登录
    def login(self):
        #s = requests.session()
        #_xsrf = BeautifulSoup(self.s.get('http://www.zhihu.com/').content).find(type='hidden')['value']
        data = {
            "_xsrf": self._xsrf,
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
        try:
            r_login = self.s.post("http://www.zhihu.com/login", data=data)
            #print(r_login.text)
        except Exception as e:
            print("login error")
            sys.exit(-1)
        r_login = self.s.get('http://www.zhihu.com')
        #print(r_login.text)
        return

    # 点赞
    def zan(self, answer_url):
        r_user_answer = self.s.get(answer_url)
        #print(r_user_answer.content)
        answer_id = BeautifulSoup(r_user_answer.content).findAll('div', attrs={'class': 'zm-item-answer '})
        for item in answer_id:
            print(item['data-aid'])
            data = {
                'method': 'vote_up',
                'params': {'answer_id': item['data-aid']},
                '_xsrf': '04c3db26d83e1de7b382f27772522f99'
            }
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
            }
            print(requests.post('http://www.zhihu.com/node/AnswerVoteBarV2', data=data))
        #print(answer_id)
        return

if __name__ == '__main__':
    robot = ZhihuRobot('weimw0417@163.com', 'admin123456')
    robot.login()
    robot.zan('http://www.zhihu.com/people/mingwei-wei/answers')


