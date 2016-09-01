#-*- coding:utf-8 -*-
'''
@author:黄鑫晨
#create_time:2016-09-01
'''
from BaseHandlerh import BaseHandler
from Database.tables import User

class Ufuncs(BaseHandler):
    def get_user_id(self, u_auth_key):
        '''
        通过用户auth_key获得id
        :param u_auth_key:
        :return: 成功则返回id,失败返回0
        '''
        try:
            user = self.db.query(User).filter(User.Uauthkey == u_auth_key).one()
            uid = user.Uid
            return uid
        except Exception,e:
            return 0


    def get_user_authkey(self, u_id):
        '''
        @attention: 直接调用时需要判断是否为0,返回0则该用户不存在
        :param u_id:
        :return:用户存在则返回u_auth_key，否则返回0
        '''
        try:
           user = self.db.query(User).filter(User.Uid == u_id).one()
           if user:
               u_auth_key = user.Uauthkey
               return u_auth_key
        except Exception, e:
            return 0


    def judge_user_valid(self, uid, u_authkey):
        #todo:可以完善区别是不合法还是用户不存在，以防止攻击
        '''
        判断用户是否合法
        :return:合法返回1，不合法返回0
        '''
        try:
            u_id = self.get_user_authkey(uid)
            if u_id == uid:
                return 1   # 合法
            else:
                return 0   # 不合法
        except Exception, e:
            print e
            return 0

    def auth_key_is_valid(self):
        