# coding=utf-8
import json

import Ufuncs
from BaseHandlerh import BaseHandler
from Database.tables import User, UCinfo
from Usermodel import userinfo_smply

class UserInfo(BaseHandler):  #获取用户自己的ID
    def post(self,):
        type = self.get_argument('type')
        if type =='10701':
            retjson={'code':'','contents':''}
            ret_content_json={}
            u_id = self.get_argument('uid')
            auth_key = self.get_argument('authkey')
            ufuncs = Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id,auth_key):   #判断用户是否有效
                try:
                   u_info = self.db.query(User).filter(User.Uid == u_id).one()
                   u_change_info = self.db.query(UCinfo).filter(UCinfo.UCuid == u_id).one()
                   #u_image = self.db.query(UserImage).filter(UserImage.UIuid == u_id).one()

                   ret_info = userinfo_smply(u_info,u_change_info)
                   ret_content_json['usermodel'] = ret_info
                   retjson['code'] ='10703'
                   retjson['contents'] = ret_content_json
                except Exception,e:
                    print e
                    retjson['code'] = '10702'
                    retjson['content'] ='用户ID不正确'

            else :
                retjson['code'] = '10704'
                retjson['contents'] = '用户授权码不正确'
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
