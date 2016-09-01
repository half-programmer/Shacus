#-*- coding:utf-8 -*-
'''
@author:黄鑫晨
#create_time:2016-09-01
'''

from  Database.tables import UserLike, User
from BaseHandlerh import BaseHandler
class UserLike(BaseHandler):
    def __init__(self):
        self.retjson={'code':'','users':''}
        self.retdata = []
    '''
      处理用户互相关注

    '''
   # def make_like(self):
    def find_my_like(self, uid):
        '''
        查询所有我关注的人
        :param uid:‘我的’Id
        :return:
        '''
        my_likes = self.db.query(UserLike).filter(UserLike.ULlikeid == uid).all()
        for my_like in my_likes:
            user_json ={'uid': '', 'ualais': '', 'usign': '', 'uimgurl': ''}
            user_json['uid'] = my_like.Uid
            user_json['ualais'] = my_like.Ualais
            user_json['usign'] = my_like.Usign
            user_json['uimgurl'] = ''
            self.retdata.append(user_json)
        self.retjson['users'] = self.retdata
        self.write(self.retjson.dumps(self.retjson, ensure_ascii=False, indent=2))


    def post(self):
        type = self.get_argument('type')
        if type == '10401':  # 用户关注
            u_id = self.get_argument('userid')
            u_authkey = self.get_argument('auth_key')
            u_likeid = self.get_argument('followerid')
            try:
                right = self.db.query(User).filter(User.Uauthkey == u_authkey).one()
                if right:
                    try:
                         exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,
                                                           UserLike.ULlikedid == u_likeid).one()
                         if exist:
                            self.retjson['code'] = '10410'
                            self.retjson['content'] = '您已经关注过该用户'
                    except Exception, e:
                         print '开始关注该用户'
                         new_userlike = UserLike(
                             ULlikeid=u_id,
                             ULlikedid=u_likeid,
                             ULvalid=1
                         )
                         self.db.merge(new_userlike)
                         try:
                           self.db.commit()
                           self.retjson['code'] = '10411'
                           self.retjson['content'] = '关注成功'
                         except Exception, e:
                            print e
                            self.rollback()
                            self.retjson['code'] = '10419'
                            self.retjson['content'] = '服务器错误'
            except Exception, e:
                print e
            self.retjson['code'] = '10412'
            self.retjson['content'] = '用户授权码不正确'
