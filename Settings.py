# -*- coding:utf-8 -*-
'''
__author__=wjl
'''
import  json

from BaseHandlerh import BaseHandler
from Database.tables import User


class PaswChange(BaseHandler):
    retjson={'code':200,'contents':'none'}
    retdata=[] #list array
    def post(self):
        type=self.get_argument("type",default="null")
        if type=='10501':
            Userid=self.get_argument("Userid","noone")
            p_password=self.get_argument("oldpassword")
           # m_password=self.get_argument("newpassword")
            data=self.db.query(User).filter(Userid==User.Uid).one()
            if data.Upassword==p_password:
                self.retjson ['code']='10501'
                self.retjson['contents']='获得修改密码权限'
            else:
                self.retjson['code']='10502'
                self.retjson['contents']='没有获得修改密码权限'
        elif type=='10511':
            Userid = self.get_argument("Userid", "noone")
            m_password = self.get_argument("newpassword")
            try:
                data = self.db.query(User).filter(Userid == User.Uid).one()
                data.Upassword = m_password
                self.db.commit()
                self.retjson['code'] = '10511'
                self.retjson['contents'] = '修改密码成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10512'
                self.retjson['contents'] = '修改密码失败'
        elif type=='10503': #修改用户昵称
                Userid = self.get_argument("Userid", "noone")
                Usernickname = self.get_argument("Usernickname", "noone")
                try:
                    data = self.db.query(User).filter(Userid == User.Uid).one()
                    data.Ualais = Usernickname
                    self.db.commit()
                    self.retjson['code'] = '10503'
                    self.retjson['contentsuy'] = '修改昵称成功'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10504'
                    self.retjson['contents'] = '修改昵称失败'
        elif type =='10505':
            Userid = self.get_argument("Userid", "noone")
            Userphone = self.get_argument("Userphone", "noone")
            try:
                data = self.db.query(User).filter(Userid == User.Uid).one()
                data.Utel = Userphone
                self.db.commit()
                self.retjson['code'] = '10505'
                self.retjson['contents'] = '修改绑定手机号成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10506'
                self.retjson['contents'] = '修改绑定手机号失败'
        elif type == '10507':
            Userid = self.get_argument("Userid", "noone")
            Userlocation = self.get_argument("Userlocation", "noone")
            try:
                data = self.db.query(User).filter(Userid == User.Uid).one()
                data.Ulocation=Userlocation
                self.db.commit()
                self.retjson['code'] = '10507'
                self.retjson['contents'] = '修改所在地成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10508'
                self.retjson['contents'] = '修改所在地失败'
        elif type == '10509':
            Userid = self.get_argument("Userid", "noone")
            Usermail = self.get_argument("Usermail", "noone")
            try:
                data = self.db.query(User).filter(Userid == User.Uid).one()
                data.Umailbox = Usermail
                self.db.commit()
                self.retjson['code'] = '10509'
                self.retjson['contents'] = '修改邮箱成功'
            except Exception, e:
                print e
                self.retjson['code'] = '10510'
                self.retjson['contents'] = '修改邮箱失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文