# -*- coding: UTF-8 -*-
__author__ = 'Wang'

'''
知乎机器人
给定用户的答案页面如‘http://www.zhihu.com/people/username/answers’
自动将该用户所有答案点赞
'''

import sys
import requests
import json
import ConfigParser
from BeautifulSoup import BeautifulSoup
from time import sleep

class ZhihuRobot:

    # 构造函数 初始化用户名密码
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.s = requests.session()
        self._xsrf = BeautifulSoup(self.s.get('http://www.zhihu.com/').content).find(type='hidden')['value']
        print(self._xsrf)

    # 登录
    def login(self):
        data = {
            "_xsrf": self._xsrf,
            "email": self.username,
            "password": self.password,
            "remember": "y"
        }
        header = {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        try:
            r_login = self.s.post("http://www.zhihu.com/login", data=data, headers=header)
        except Exception as e:
            print("login error")
            sys.exit(-1)
        r_login = self.s.get('http://www.zhihu.com')
        #print(r_login.text)
        return

    # 点赞
    def zan(self, answer_url):
        r_user_answer = self.s.get(answer_url)
        answer_id = BeautifulSoup(r_user_answer.content).findAll('div', attrs={'class': 'zm-item-answer '})
        _xsrf = BeautifulSoup(r_user_answer.content).find('input', attrs={'name': '_xsrf'})['value']
        #print(self._xsrf)
        #print(_xsrf)
        for item in answer_id:
            print(item['data-aid'])
            # 以下对params进行json处理是胜败的关键 之前一直返回400 改完这个就200了
            params = json.dumps({
                'answer_id': item['data-aid']
            })
            data = {
                'method': 'vote_up',
                'params': params,
                '_xsrf': _xsrf
            }
            header = {
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'www.zhihu.com',
                'Origin': 'http://www.zhihu.com',
                'Referer': 'http://www.zhihu.com/people/mingwei-wei/answers',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            print(self.s.post('http://www.zhihu.com/node/AnswerVoteBarV2', data=data, headers=header, timeout=10))
            sleep(2)

        return

    def textini(self):
        cf = ConfigParser.ConfigParser()
        cf.read('settings.ini')
        headers = cf._sections['headers']
        email = cf.get("info", "email")
        password = cf.get("info", "password")
        print(headers)
        print(email)
        print(password)

if __name__ == '__main__':
    robot = ZhihuRobot('weimw0417@163.com', 'admin123456')
    #robot.login()
    #robot.zan('http://www.zhihu.com/people/wuxu92/answers')
    robot.textini()


