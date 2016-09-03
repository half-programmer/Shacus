# coding=utf-8

'''
@author   兰威
@type     用户订单
'''
from BaseHandlerh import BaseHandler
from Userinfo import Ufuncs


# class UserIndent(BaseHandler):
#     retjson ={'code':'', 'contents':''}
#     def post(self):
#         type = self.get_argument('type')
#         if type == '10309':
#             u_id = self.get_argument('uid')
#             auth_key = self.get_argument('authkey')
#             ufuncs = Ufuncs.Ufuncs()
#             if ufuncs.judge_user_valid(u_id,auth_key):
#
#             else :
#                 self.retjson['code'] = '10391'
#                 self.retjson['contents'] = ''