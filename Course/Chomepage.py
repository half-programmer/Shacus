# coding=utf-8

'''
@兰威
2016.9.6
'''
from BaseHandlerh import BaseHandler
from Userinfo import Ufuncs


class Chomepage(BaseHandler):# 教程首页
    retjson ={ "code": '','contents':''}

    def post(self):
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufuncs = Ufuncs()
        if ufuncs.judge_user_valid(u_id,u_authkey):
            type = self.get_argument('type')
            if type == '11001':  #查看教程首页


        else :
            self.retjson['contents'] = '用户授权码不正确'
            self.retjson['code'] = '11000'
