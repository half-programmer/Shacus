# coding=utf-8

'''
@兰威
2016.9.6
'''
from BaseHandlerh import BaseHandler
from Userinfo import Ufuncs


class Chomepage(BaseHandler):# 教程首页

    def post(self):
        ufuncs = Ufuncs()
        if ufuncs.judge_user_valid()