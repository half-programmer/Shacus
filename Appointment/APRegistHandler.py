# coding=utf-8
import json
from  BaseHandlerh import BaseHandler
from Database.tables import User, AppointEntry


class APregistHandler(BaseHandler):  # 报名约拍
    retjson = {'code': '', 'contents': ''}

    def post(self):
        ap_registe_type = self.get_argument('type')
        if ap_registe_type == '10271':
            auth_key = self.get_argument('authkey')
            ap_id = self.get_argument('apid')
            try:
                ap_user = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                ap_user_id = ap_user.Uid
                try :
                    exist = self.db.query(AppointEntry).\
                    filter(AppointEntry.AEregisterID == ap_user_id and AppointEntry.AEapid == ap_id).one() # 应该再加上和ap_id的验证
                    if exist:
                        self.retjson['contents'] = '已报名过该约拍'
                        self.retjson['code'] = '10270'
                except Exception,e:
                    new_appointmententry = AppointEntry(
                        AEapid = ap_id,
                        AEregisterID = ap_user_id,
                        AEvalid = 1,
                        AEchoosed = 0
                    )
                    self.db.merge(new_appointmententry)
                    try :
                        self.db.commit()
                        self.retjson['contents'] = '用户报名成功'
                        self.retjson['code'] = '10273'
                    except Exception,e:
                        print e
                        self.db.rollback()
                        self.retjson['contents'] = '数据库插入错误'
                        self.retjson['code'] = '10274'
            except Exception,e:
                print e
                self.retjson['contents'] = '授权码不存在或已过期'
                self.retjson['code'] = '10279'
        if ap_registe_type == '10252': #用户取消报名
            auth_key = self.get_argument('authkey')
            ap_id = self.get_argument('apid')
            try:
                ap_user = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                ap_user_id = ap_user.Uid
                try:
                    exist = self.db.query(AppointEntry).filter(
                        AppointEntry.AEregisterID == ap_user_id and AppointEntry.AEapid == ap_id).one()  # todo应该再加上和ap_id的验证
                    if exist.AEvalid:
                        self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == ap_user_id).\
                            update({AppointEntry.AEvalid == 0})
                        try :
                            self.db.commit()
                            self.retjson['contents'] = '取消报名成功'
                            self.retjson['code'] = '10275'
                        except Exception,e:
                            print e
                            self.db.rollback()
                            self.retjson['contents'] = '数据库更新错误'
                            self.retjson['code'] = '10274'
                    else :
                        self.retjson['contents'] = '用户已经取消报名'
                        self.retjson['code'] = '10276'
                except Exception, e:
                    self.retjson['contents'] = '用户未报名过该约拍'
                    self.retjson['code'] = '10277'
            except Exception, e:
                print e
                self.retjson['contents'] = '授权码不存在或已过期'
                self.retjson['code'] = '10279'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
