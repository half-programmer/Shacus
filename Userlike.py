# -*- coding:utf8 -*-

from BaseHandlerh import BaseHandler
from Database.tables import UserLike,User
from Userinfo import Ufuncs
'''
兰威
2016.09.01
'''
'''
@author:黄鑫晨
@type:用户收藏
@time:2019-09-02
'''

class Userlike(BaseHandler):
    retjson = {'code': '','content':'none'}

    def post(self):
        type = self.get_argument('type')
        if type == '10401':   #用户关注
            u_id = self.get_argument('userid')
            u_authkey = self.get_argument('auth_key')
            u_likeid = self.get_argument('followerid')
            try:
                right = self.db.query(User).filter(User.Uauthkey == u_authkey).one()
                if right :
                    try:
                        exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,UserLike.ULlikedid == u_likeid).one()
                        if exist :
                            self.retjson['code'] = '10410'
                            self.retjson['content'] = '您已经关注过该用户'
                    except Exception,e :
                        print '开始关注该用户'
                        new_userlike = UserLike(
                            ULlikeid = u_id,
                            ULlikedid = u_likeid,
                            ULvalid = 1
                        )
                        self.db.merge(new_userlike)
                        try :
                            self.db.commit()
                            self.retjson['code'] ='10411'
                            self.retjson['content'] = '关注成功'
                        except Exception,e:
                            print e
                            self.rollback()
                            self.retjson['code'] = '10419'
                            self.retjson['content'] = '服务器错误'
            except Exception,e:
                print e
                self.retjson['code'] = '10412'
                self.retjson['content'] = '用户授权码不正确'








