# coding=utf-8
import json

import Userinfo.Ufuncs
from BaseHandlerh import BaseHandler
from Database.tables import Favorite

'''
@author:黄鑫晨
@type:用户收藏
@time:2019-09-02
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
        typeid = self.get_argument('typeid')
        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(user_id, u_auth_key):
            favorite = Favorite(
                Fuid=user_id,
                Ftype=1,  # 1为约拍
                Ftypeid=typeid,
                Fvalid=1
                )
            self.db.merge(favorite)
            self.db.commit()
            self.retjson['contents'] = r'收藏成功'
        else:
            self.retjson['contents'] = r'收藏失败'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

