# coding=utf-8
'''
用户点赞表
@author: 黄鑫晨
'''
from BaseHandlerh import BaseHandler
from Database.tables import Appointment, AppointLike
from Userinfo.Ufuncs import Ufuncs
class APprase(BaseHandler):
    retjson = {'code':'','content':''}
    def post(self):
        type = self.get_argument('type')
        type_id = self.get_argument('type_id')
        uid = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        if Ufuncs.judge_user_valid(uid,u_authkey):
            if type == '10601':  # 对约拍进行点赞
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == type_id).one()
                    if appointment.APvalid == 0:
                        self.retjson['content'] = r"该约拍已失效"
                    else:  # 查找是否已经点过赞
                        try:
                            once_liked = self.db.query(AppointLike).filter(AppointLike.ALapid == type_id, AppointLike.ALuid == uid).one()
                            if once_liked:
                                if once_liked.ALvalid == 1:
                                    self.retjson['code'] = '10605'
                                    self.retjson['content'] = r'已点过赞'
                                else:  # 曾经点过赞，但是已经取消
                                    self.retjson['code'] = '10600'
                                    self.retjson['content'] = r'点赞成功'
                        except Exception, e:
                            print e
                            new_Aplike = AppointLike(
                                ALapid=type_id,
                                ALuid=uid,
                                ALvalid=1
                            )
                            self.db.merge(new_Aplike)
                            try:
                                self.db.commit()
                                self.retjson['code'] = '10600'
                                self.retjson['content'] = r'点赞成功!'
                            except Exception, e:
                                self.retjson['code'] = '10606'
                                self.retjson['content'] = r'数据库提交出错'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10607'
                    self.retjson['content'] = '该约拍不存在或已过期'
        else:
            self.retjson['code'] = '10608'
            self.retjson['content'] = '用户认证失败'