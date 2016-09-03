# coding=utf-8
'''
  @author:黄鑫晨
  2016.08.29   2016.09.03
'''
import json

import Userinfo
from APmodel import APmodelHandler
from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User
from Userinfo import Ufuncs


class APaskHandler(BaseHandler):  # 请求约拍相关信息

    # todo:返回特定条件下的约拍
    retjson = {'code': '', 'contents': ''}


    def no_result_found(self, e):
        print e
        self.retjson['code'] = '10251'
        self.retjson['contents'] = '未查询到约拍记录'

    def ap_ask_user(self, user):  # 查询指定用户的所有约拍
        '''
        :param user: 传入一个User对象
        :return: 无返回，直接修改retjson
        '''
        uid = user.Uid
        try:
            appointments = self.db.query(Appointment).filter(Appointment.APsponsorid == uid).all()
            APmodelHandler.ap_Model_simply(appointments, self.retdata)
            self.retjson['contents'] = self.retdata
        except Exception, e:
            print e
            self.no_result_found(e)

    def post(self):
        u_auth_key = self.get_argument('authkey')
        request_type = self.get_argument('type')
        u_id = self.get_argument('uid')

        # if Ufuncs.judge_user_valid(u_id,u_auth_key): # 授权码正确
        #     ppointments = self.db.query(Appointment). \
        #         #             filter(Appointment.APtype == 1, Appointment.APclosed == 0).all()
        # else:
        self.retjson['contents'] = '授权码不存在或已过期'
        self.retjson['code'] = '10214'
        # if request_type == '10231':  # 请求所有设定地点的摄影师发布的约拍中未关闭的
        #     try:
        #         appointments = self.db.query(Appointment). \
        #             filter(Appointment.APtype == 1, Appointment.APclosed == 0).all()
        #         APmodelHandler.ap_Model_simply(appointments, self.retdata)
        #         self.retjson['contents'] = self.retdata
        #     except Exception, e:
        #         self.no_result_found(e)
        # elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍中未关闭的
        #     try:
        #         appointments = self.db.query(Appointment). \
        #             filter(Appointment.APtype == 0, Appointment.APclosed == 0).all()
        #         APmodelHandler.ap_Model_simply(appointments, self.retdata)
        #         self.retjson['contents'] = self.retdata
        #     except Exception, e:
        #         self.no_result_found(e)
        # elif request_type == '10240':  # 请求用户自己发布的所有约拍
        #     try:
        #         user = self.db.query(User).filter(User.Uauthkey == auth_key).one()
        #         self.ap_ask_user(user)
        #     except Exception, e:
        #         self.retjson['contents'] = '授权码不存在或已过期'
        #         self.retjson['code'] = '10214'
        # elif request_type == '10241':  # 请求指定用户发布的所有约拍
        #     uid = self.get_argument('uid')  # 指定用户的id
        #     try:
        #         user = self.db.query(User).filter(User.Uid == uid).one()
        #         self.ap_ask_user(user)
        #     except Exception, e:
        #         self.retjson['contents'] = '授权码不存在或已过期'
        #         self.retjson['code'] = '10214'

        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, u_auth_key):

            if request_type == '10231':  # 请求所有设定地点的摄影师发布的约拍中未关闭的
                retdata = []
                try:
                    appointments = self.db.query(Appointment). \
                        filter(Appointment.APtype == 1, Appointment.APclosed == 0, Appointment.APvalid == 1).all()
                    APmodelHandler.ap_Model_simply(appointments, retdata)
                    self.retjson['code'] = '10250'
                    self.retjson['contents'] = retdata
                except Exception, e: # 没有找到约拍
                    self.no_result_found(e)
            elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍中未关闭的
                retdata = []
                try:
                    appointments = self.db.query(Appointment). \
                        filter(Appointment.APtype == 0, Appointment.APclosed == 0, Appointment.APvalid == 1).all()
                    APmodelHandler.ap_Model_simply(appointments, retdata)
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.no_result_found(e)
            elif request_type == '10241':  # 请求指定用户发布的所有约拍
                find_uid = self.get_argument('finduid')  # 指定用户的id
                try:
                    user = self.db.query(User).filter(User.Uid == find_uid).one()
                    self.ap_ask_user(user)
                except Exception, e:
                    self.retjson['contents'] = '授权码不存在或已过期'
                    self.retjson['code'] = '10214'
        else:
            self.retjson['contents'] = '授权码不存在或已过期'
            self.retjson['code'] = '10214'

        #
        #
        #

        #
        # elif request_type == '10270':#在报名约拍中的人里选择约拍对象
        #    # uid = self.get_argument("uid",default="none")
        #
        #     m_AEapid=self.get_argument("AEapid",default="null")
        #     try:
        #         data=self.db.query(AppointEntry).filter(AppointEntry.AEapid==m_AEapid,AppointEntry.AEvalid==1).all()
        #         for item in data:
        #             ApInfo=self.db.query(User).filter(User.Uid==item.AEregisterID).one()
        #             ApImage=self.db.query(UserImage).filter(UserImage.UIuid==item.AEregisterID).one()
        #             APinfoFuncion.APinfochoose(ApInfo, ApImage, self.retdata)
        #             self.retjson['contents']= self.retdata
        #             self.retjson['code']='12703'
        #
        #     except Exception, e:
        #             print e
        #             self.retjson['contents']='选择约拍对象失败'
        #             self.retjson['code']='10270'
        # elif request_type == '10271':
        #    # choose = True
        #     m_APid=self.get_argument("APid",default="null")
        #     m_AEregisterid=self.get_argument("AEregisterid",default="null")
        #     m =int(m_AEregisterid)
        #     try:
        #         #data=self.db.query(AppointEntry).filter(AppointEntry.AEapid == m_APid and AppointEntry.AEregisterID == m_AEregisterid).one()
        #         data=self.db.query(AppointEntry).filter(AppointEntry.AEapid == m_APid and AppointEntry.AEregisterID == m).one()
        #         data.AEchoosed = True
        #         self.db.commit()
        #         self.retjson["code"]="10271"
        #         self.retjson["contents"]="选择成功！"
        #     except Exception, e:
        #         print e
        #         self.retjson['contents'] = '选择约拍对象失败'
        #         self.retdata['code'] = '10271'
        #
        # elif request_type =='10261':   #查看自己报名的约拍的结果
        #     uid = self.get_argument('uid')
        #     ap_id = self.get_argument('apid')
        #     try:
        #         u_result = self.db.query(AppointEntry.AEchoosed).\
        #             filter(AppointEntry.AEapid ==ap_id and AppointEntry.AEregisterID == uid).one()
        #         self.retjson['code'] = '10263'
        #         self.retjson['contents'] = u_result[0]
        #     except Exception,e:
        #         print e
        #         self.retjson['code'] = '10262'
        #         self.retjson['contents'] = '用户未参加此约拍的报名'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

