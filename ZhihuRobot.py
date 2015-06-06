# -*- coding: UTF-8 -*-
__author__ = 'Wang'

'''
知乎机器人
给定用户的答案页面如‘http://www.zhihu.com/people/username/answers’
自动将该用户所有答案点赞

知乎的赞统计似乎不是实时的
当下点了一堆赞要在隔较长时间（一天左右）后又有人点了个赞时才将当前两次的赞数汇总到个人主页总赞数
刚试了一下又实时更新了 啊啊啊什么鬼

知乎的感谢数是实时更新的
'''

import sys
import requests
import json
import ConfigParser
from BeautifulSoup import BeautifulSoup
from time import sleep

class ZhihuRobot:

    # 构造函数 初始化用户名 密码 session _xsrf
    def __init__(self, username=0, password=0):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('config.ini')
        if username == 0 and password == 0:
            self.username = self.cf.get("info", "email")
            self.password = self.cf.get("info", "password")
        else:
            self.username = username
            self.password = password
        self.s = requests.session()
        self._xsrf = BeautifulSoup(self.s.get('http://www.zhihu.com/').content).find(type='hidden')['value']
        print(self.username)
        print(self.password)

    # 登录
    def login(self):
        data = {
            "_xsrf": self._xsrf,
            "email": self.username,
            "password": self.password,
            "remember": "y"
        }
        headers = dict(self.cf._sections['headers'])
        try:
            r_login = self.s.post("http://www.zhihu.com/login", data=data, headers=headers)
        except Exception as e:
            print("login error", e)
            sys.exit(-1)
        # 登录成功后跳转 没有这句应该也可以
        r_login = self.s.get('http://www.zhihu.com')
        return

    # 点赞
    def zan(self, answer_url):
        r_user_answer = self.s.get(answer_url)
        # 得到该用户答案的id列表 并重新获得_xsrf
        answer_id = BeautifulSoup(r_user_answer.content).findAll('div', attrs={'class': 'zm-item-answer '})
        _xsrf = BeautifulSoup(r_user_answer.content).find('input', attrs={'name': '_xsrf'})['value']
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
            headers = dict(self.cf._sections['headers'])
            print(self.s.post('http://www.zhihu.com/node/AnswerVoteBarV2', data=data, headers=headers, timeout=10))
            sleep(5)
        return

    # 感谢
    def thanks(self, answer_url):
        r_user_answer = self.s.get(answer_url)
        answer_id = BeautifulSoup(r_user_answer.content).findAll('div', attrs={'class': 'zm-item-answer '})
        _xsrf = BeautifulSoup(r_user_answer.content).find('input', attrs={'name': '_xsrf'})['value']
        for item in answer_id:
            data = {
                'aid': item['data-aid'],
                '_xsrf': _xsrf
            }
            headers = dict(self.cf._sections['headers'])
            print(self.s.post('http://www.zhihu.com/answer/thanks', data=data, headers=headers))
            sleep(5)
        return

    # 读取多个用户
    def test_muluser(self):
        userlist = self.cf.get("user-list", "username").split(",")
        passwordlist = self.cf.get("password-list", "password").split(",")
        for i in range(len(userlist)):
            print(userlist[i], passwordlist[i])
        return

    # 获取特定用户所有回答页面
    def zan_allanswer(self, answer_url):
        r_user_answer = self.s.get(answer_url)
        zm_invite_pager = BeautifulSoup(r_user_answer.content).find("div", attrs={"class": "zm-invite-pager"})
        if zm_invite_pager == "":
            return answer_url
        else:
            if zm_invite_pager.find("span")['value'] == "上一页":
                t = zm_invite_pager.find("span")[-2]

        return

if __name__ == '__main__':
    #robot = ZhihuRobot('english_a5@126.com', 'admin123456')
    robot = ZhihuRobot()
    robot.login()
    #robot.zan('http://www.zhihu.com/people/liu-yuan-bo-56/answers')
    robot.thanks('http://www.zhihu.com/people/mingwei-wei/answers')
    #robot.test_muluser()
    #robot.zan_allanswer('http://www.zhihu.com/people/ccbikai/answers')


