# coding=utf-8
import json

import Userinfo.Ufuncs
from Appointment.APmodel import APmodelHandler
from BaseHandlerh import BaseHandler
from Database.tables import Favorite, Appointment

'''
@author:黄鑫晨
@type:用户收藏
@time:2019-09-02
@attention:用户客户端无法多次收藏或取消一个活动等，并且也不会影响，所以为了速度未写判断
'''
class UserFavorite(BaseHandler):
    retjson = {'code': '', 'contents': ''}
    '''
     用户收藏表
    '''
    def post(self):
        type = self.get_argument('type')
        user_id = self.get_argument('uid')
        u_auth_key = self.get_argument('authkey')
        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(user_id, u_auth_key):
            if type == '10501': # 收藏约拍
                typeid = self.get_argument('typeid')
                try:
                    exist =  self.db.query(Appointment).filter(Appointment.APid == typeid).one()
                    if exist: # 该约拍存在
                        if exist.APvalid == 1:
                            favorite = Favorite(
                                Fuid=user_id,
                                Ftype=1,  # 1为约拍
                                Ftypeid=typeid,
                                Fvalid=1
                                 )
                            self.db.merge(favorite)
                            try:
                                 self.db.commit()
                                 self.retjson['code'] = '10520'
                                 self.retjson['contents'] = r'收藏成功'
                            except Exception,e:
                                 #todo 基本码待定
                                 self.retjson['contents'] = r'数据库操作失败，请重试'
                        else:
                            self.retjson['code'] = '10525'
                            self.retjson['contents'] = r'该约拍已过期'
                except Exception,e:
                    print e
                    self.retjson['code'] = '10524'
                    self.retjson['contents'] = r'该约拍不存在！'
            if type == '10510':  # 取消收藏约拍
                typeid = self.get_argument('typeid')
                try:
                    self.db.query(Favorite).filter(Favorite.Fuid == user_id, Favorite.Ftypeid ==typeid).\
                        update({Favorite.Fvalid: 0}, synchronize_session=False)
                    self.retjson['code'] = '10520'
                    self.retjson['contents'] = r'取消收藏约拍成功'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10522'
                    self.retjson['contents'] = r'用户未关注此约拍'
            if type == '10541': # 查看所有收藏的活动
                try:
                    retdata = []
                    favorites = self.db.query(Favorite).filter(Favorite.Fuid == user_id).all()  # 返回收藏的所有活动
                    for each_favorite in favorites:
                        retdata.append(APmodelHandler.ap_Model_simply(each_favorite))
                    self.retjson['code'] = '10550'
                    self.retjson['contents'] = retdata
                except Exception,e:
                    self.retjson['code'] = '10526'
                    self.retjson['contents'] = r'用户未收藏任何约拍'
        else:
            self.retjson['code'] = '10521'
            self.retjson['contents'] = r'用户认证错误！操作失败'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

