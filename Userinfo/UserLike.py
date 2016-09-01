#-*- coding:utf-8 -*-
'''
@author:黄鑫晨
#create_time:2016-09-01
'''
import json

from  Database.tables import UserLike, User
from BaseHandlerh import BaseHandler
from Ufuncs import Ufuncs
class FindUlike(BaseHandler):

    def __init__(self):
        self.retjson={'code' : '', 'contents': ''}
        self.retdata = []
    '''
      处理用户互相关注

    '''
    def post(self):
        u_auth_key = self.get_argument('authkey')
        u_id = self.get_argument('uid')
        type = self.get_argument('type')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):
            if type == '10403':  #查询所有我关注的人
                self.find_my_like(u_id)
            if type =='10401':   #关注某一人
                followerID = self.get_argument("followerid")
                self.follow_user(u_id,followerID)
            if type =='10402': #取消关注某一人
                followerID = self.get_argument("followerid")
                self.not_follow_user(u_id, followerID)


        else:
            self.retjson['code'] = '10412'
            self.retjson['contents'] = '用户不合法'
            self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 在当前目录下生成retjson文件输出中文






    def find_my_like(self, uid):
        '''
        查询所有我关注的人
        :param uid:‘我的’Id
        :return:
        '''
        try:
            my_likes = self.db.query(UserLike).filter(UserLike.ULlikeid == uid).all()

            for my_like in my_likes:
                user_json = {'uid': my_like.Uid, 'ualais': my_like.Ualais, 'usign': my_like.Usign, 'uimgurl': ''}
                self.retdata.append(user_json)
                self.retjson['contents'] = self.retdata
        except Exception,e:
            self.retjson['code'] = '10421'
            self.retjson['contents'] = r'该用户没有关注任何人'
        self.write(self.retjson.dumps(self.retjson, ensure_ascii=False, indent=2))



    def follow_user(self,u_id,follower_id):
            try:
                exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,
                                                           UserLike.ULlikedid == follower_id).one()
                if exist:
                        self.retjson['code'] = '10410'
                        self.retjson['contents'] = '您已经关注过该用户'
            except Exception, e:
                    print '开始关注该用户'
                    new_userlike = UserLike(
                        ULlikeid=u_id,
                        ULlikedid=follower_id,
                        ULvalid=1
                         )
                    self.db.merge(new_userlike)
                    try:
                        self.db.commit()
                        self.retjson['code'] = '10411'
                        self.retjson['contents'] = '关注成功'
                    except Exception, e:
                        print e
                        self.rollback()
                        self.retjson['code'] = '10419'
                        self.retjson['contents'] = '服务器错误'

    def not_follow_user(self,u_id,follower_id):
        try:
            exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,
                                                   UserLike.ULlikedid == follower_id).one()
            if exist:
                exist.ULvalid = 0
                try:
                    self.db.commit()
                    self.retjson['contents'] = '取消关注成功'
                    self.retjson['code'] = '10420'
                except Exception,e :
                    print e
                    self.db.rollback()
                    self.retjson['code'] = '10419'
                    self.retjson['contents'] = '服务器错误'
        except Exception,e :
            print e
            self.retjson['contents'] = '未关注该用户'
            self.retjson['code'] = '10421'
