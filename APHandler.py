# coding=utf-8
'''
  黄鑫晨
  2016.08.29

'''
import json
import types

import AppFuncs
from FileHandler.Upload import AuthKeyHandler
from  BaseHandlerh import BaseHandler
from Database.tables import Appointment, User,Verification
from AppFuncs import response

class AppcreateHandler(BaseHandler):  # 创建约拍
    retjson = {'code': '400', 'contents': 'None', 'Code': ''}
    def post(self):
        # 10201 客户端请求，摄影师发布约拍  start

        ap_type = self.get_argument('type')
        if ap_type == '10201' or ap_type == '10202': # 请求获得上传权限
            print '进入10201'
            user_phone = self.get_argument('phone')
            auth_key = self.get_argument('auth_key')
            ap_title = self.get_argument('title')
            ap_imgs = self.get_argument('imgs')
            try:
                sponsor = self.db.query(User).filter(User.Utel == user_phone).one()
                key = sponsor.Uauthkey
                ap_sponsorid = sponsor.Uid
                if auth_key == key:  #认证成功
                    try:
                        appointment = self.db.query(Appointment).filter(Appointment.APtitle == ap_title).one()
                        if appointment:
                            self.retjson['Code'] = '10210'
                            self.retjson['contents'] = r'该约拍已存在'
                    except Exception, e:
                        print e
                        retjson_body = {'auth_key': '', 'apId': ''}
                        auth_key_handler = AuthKeyHandler()
                        ap_imgs_json =json.loads(ap_imgs)
                        retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)
                        self.retjson['code'] = 200
                        self.retjson['Code'] = 10200

                        new_appointment = Appointment(
                            APtitle=ap_title,
                            APsponsorid=sponsor.Uid,
                            APtype=ap_type,
                            APlocation='',
                            APstartT='',
                            APendT='',
                            APcontent='',  # 活动介绍
                            APclosed=0,
                            APlikeN=0,
                            APvalid=1,
                            APaddallowed=0
                        )
                        self.db.merge(new_appointment)
                        self.db.commit()
                        ap_id = self.db.query(Appointment.APid).filter(
                            Appointment.APtitle == ap_title and Appointment.APsponsorid == ap_sponsorid).one()
                        retjson_body['apId'] = ap_id
                        self.retjson['contents'] = retjson_body
                else:
                    self.retjson['Code'] = '10211'
                    self.retjson['contents'] = r'用户认证码错误'
            except Exception,e:
                print e
                self.retjson['Code'] = '10212'
                self.retjson['contents']="该用户名不存在"
        elif ap_type == '10205': # 开始传输数据
            print "进入10205"
            ap_id = self.get_argument('apid')
            auth_key = self.get_argument('auth_key')
            # todo: auth_key经常使用，可以优化
            ap_title = self.get_argument('title')
            ap_start_time = self.get_argument('start_time')
            ap_end_time = self.get_argument('end_time')
            ap_join_time = self.get_argument('join_time')
            ap_location = self.get_argument('location')
            ap_free = self.get_argument('free')
            ap_price = self.get_argument('price')
            ap_content = self.get_argument('contents')
            ap_tag = self.get_argument('tags')  # 约拍标签？确认长度
            ap_addallowed = self.get_argument('ap_allowed')
            ap_type = self.get_argument('ap_type')
            try:
                uid = self.db.query(User.Uid).filter(User.Uauthkey == auth_key).first() # 查看该用户id
                try:
                    exist = self.db.query(Appointment).filter(Appointment.APtype == ap_type,
                                                          Appointment.APtitle == ap_title,
                                                          Appointment.APsponsorid == uid
                                                              ).one()  # 判断该活动是否已经存在
                    if exist:
                        self.retjson['Code'] = '10210'
                        self.retjson['contents'] = '该约拍已存在'
                except Exception, e:
                    print e
                    try:
                        exist = self.db.query(Appointment).filter(Appointment.APid == ap_id,
                                                              Appointment.APtitle == ap_title
                                                              ).one()
                        if exist:
                            if uid == ap_id:
                                self.db.query(Appointment).filter(Appointment.APid == ap_id). \
                                    update({Appointment.APstartT: ap_start_time, Appointment.APendT: ap_end_time,
                                        Appointment.APjoinT: ap_join_time,
                                        Appointment.APlocation: ap_location, Appointment.APfree: ap_free,
                                        Appointment.APprice: ap_price, Appointment.APcontent: ap_content,
                                        Appointment.APtag: ap_tag, Appointment.APaddallowed: ap_addallowed,
                                        Appointment.APtype: ap_type
                                        }, synchronize_session=False)
                                self.db.commit()
                                self.retjson['code'] = '200'
                                self.retjson['Code'] = '10206'
                                self.retjson['contents'] = '发布约拍成功'
                    except Exception, e:
                        print e
                        self.retjson['Code'] = '10206'
                        self.retjson['contents'] = r'该发布尚未获得权限！'
            except Exception, e:
                print e
                self.retjson['contents'] = r'用户授权码错误！'

        else:
            print 'ap_type: ', ap_type

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))



        # 判断返回是否许可

        # 10201 客户端请求，摄影师发布约拍 end

class ApregistHandler(BaseHandler):  # 报名约拍
    def __init__(self):
        self.retjson = {'code': '', 'Code': '', 'contents': ''}
    def post(self):
        auth_key = self.get_argument('authkey')


class APaskHandler(BaseHandler): # 请求约拍相关信息
    retjson = {'code': '400', 'Code': '', 'contents': ''}
    retdata = []
    def no_result_found(self,e):
        print e
        self.retjson['code'] = 400
        self.retdata = 'no result found'

    def post(self):
        auth_key = self.get_argument('authkey')
        request_type = self.get_argument('type')
        if request_type == '10231': # 请求所有设定地点的摄影师发布的约拍中未关闭的
            try:
                appointments = self.db.query(Appointment).filter(Appointment.APtype == 1, Appointment.APclosed == 0).all()
                AppFuncs.response(appointments, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception, e:
                self.no_result_found(e)
        elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍
            try:
                appointments = self.db.query(Appointment).filter(Appointment.APtype == 2).all()
                AppFuncs.response(appointments, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception, e:
                self.no_result_found(e)
        elif request_type == '10240':  # 请求用户自己发布的所有约拍
            ap_sponsorid = self.get_argument('sponsorid')
            try:
                appointments = self.db.query(Appointment).filter(Appointment.APsponsorid == ap_sponsorid).all()
                AppFuncs.response(appointments, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception, e:
                self.no_result_found(e)

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
            # if type == 'AskMyAppointments':  # 1.请求我发布的所有约拍
            #     userID = self.get_argument('userID', default='unsolved')
            #     try:
            #         data = self.db.query(Appointment).filter(Appointment.sponsorID == userID).all()
            #         AppointmentFunctions.response(data, self.retdata)
            #     except:
            #         self.retjson['code'] = 400
            #         self.retdata = 'no result found'


            # elif type == 'AskOpenAppointments':  # 3.获得所有未关闭约拍
            #     userID = self.get_argument('userID', default='unsolved')
            #     try:
            #         appointments = self.db.query(Appointment).filter(Appointment.closed == False).all()  # 返回所有未关闭约拍
            #         AppFuncs.response(appointments, self.retdata)
            #     except:
            #         self.retjson['code'] = 400
            #         self.retdata = 'no result found'
            # elif type == 'AskParticipants':  # 4.获得某个约拍的所有报名者（包括自己的约拍）
            #     userID = self.get_argument('userID', default='unsolved')
            #     appointmentID = self.get_argument('appointmrntID', default='unsolved')  # 约拍ID
            #     try:
            #         registers = self.db.query(AppointmentRegister).filter(
            #             AppointmentRegister.appointmentID == appointmentID).all()  # 某个约拍所有报名者
            #         for user in registers:
            #             response = user.userID
            #             AppointmentFunctions.response(response, self.retdata)
            #     except:
            #         self.retjson['code'] = 400
            #         self.retdata = 'no result found'
            #
            # self.retjson['content'] = retdata
            # self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

# class RegistAppointment(BaseHandler):  # 报名约拍
#     def post(self):
#         m_user = self.get_argument('userID', default='unsolved')
#         m_appointment_number = self.get_argument('appointmentID', default='unsolved')  # 想报名的活动
#         retjson = {'code': '400', 'content': 'None'}
#         try:
#             appointment = self.db.query(Appointment).filter(Appointment.appointmentID == m_appointment_number).one()
#             if not appointment.closed:  # 活动未关闭
#                 if m_user != appointment.sponsorID:  # 不是发布人
#                     try:
#                         if self.db.query(AppointmentRegister).filter(
#                                         AppointmentRegister.appointmentID == m_appointment_number,
#                                         AppointmentRegister.registerID == m_user).one():  # 已经报过名
#                             retjson['content'] = '不能重复报名'
#                     except:
#                         new_register = AppointmentRegister(
#                             appointmentID=m_appointment_number,
#                             registerID=m_user
#                         )
#                         self.db.merge(new_register)  # 在报名人中加入该项
#                         retjson['code'] = 200
#                         retjson['content'] = '报名成功'
#                         commonFunctions.commit(self, retjson)  # 提交
#                 else:
#                     retjson['code'] = 400
#                     retjson['content'] = '不能报名自己发布的活动'
#             else:
#                 retjson['code'] = 400
#                 retjson['content'] = '该活动已关闭'
#         except:
#             retjson['code'] = 400
#             retjson['content'] = '该活动不存在或未登陆'
#
#         self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # ensure_ascii:允许中文
#
#
#         # self.db.query(Appointment).filter(Appointment.appointmentID == m_appointment_number).update({"closed": True})  #
