# coding=utf-8
'''
  黄鑫晨&&兰威
  2016.08.29

'''
import json
import commonFunctions
from FileHandler.Upload import auth_token
from  BaseHandlerh import BaseHandler
from Database.tables import Appointment, User,Verification


class CreateAppointment(BaseHandler):  # 创建约拍
    retjson = {'code': '400', 'contents': 'None', 'Code': ''}
    def post(self):
        # 10201 客户端请求，摄影师发布约拍  start

        ap_type = self.get_argument('type')
        if type == 10201 or 10202: # 请求获得上传权限
            user_phone = self.get_argument('phone')
            auth_key = self.get_argument('auth_key')
            ap_title = self.get_argument('title')
            try:
                sponsor = self.db.query(User).filter(User.Utel == user_phone).one()
                key = sponsor.Uauthkey
                print "key: ", key
                print "auth_key: ", auth_key
                ap_sponsorid = sponsor.Uid
                # todo 判断该活动是否存在
                if auth_key == key:  #认证成功
                    try:
                        appointment = self.db.query(Appointment).filter(Appointment.APtitle == ap_title).one()
                        if appointment:
                            self.retjson['contents'] = '该约拍已存在'
                    except Exception, e:
                        print e
                        upload_auth_token = auth_token  # 上传授权凭证
                        retjson_body = {'auth_key': upload_auth_token, 'apId':''}
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
                            APvalid=1)
                        self.db.merge(new_appointment)
                        self.db.commit()
                        ap_id = self.db.query(Appointment.APid).filter(
                            Appointment.APtitle == ap_title and Appointment.APsponsorid == ap_sponsorid).one()
                        retjson_body['apId'] = ap_id
                        self.retjson['contents'] = retjson_body
                else:
                    self.retjson['contents'] = '用户认证码错误'
            except Exception,e:
                print e
                self.retjson['contents']="该用户名不存在"
        # elif type == 10205: # 开始传输数据
        #      user_phone = self.get_argument('phone')
        #      auth_key = self.get_argument('auth_key')
        #      title = self.get_argument('title')


            self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))



        # 判断返回是否许可

        # 10201 客户端请求，摄影师发布约拍 end


        # m_appointment_title = self.get_argument('appointmentTitle') # 标题
        # m_sponsorid = self.get_argument('sponsorID')  # 发起人
        # m_location = self.get_argument('location')  # 位置
        # m_start_time = self.get_argument('startTime')
        # m_end_time = self.get_argument('endTime')
        #
        # m_appointment_introduction = self.get_argument('appointmentIntroduction')
        # m_self_introduction = self.get_argument('selfIntroduction')  # 自我介绍
        # m_styleID = self.get_argument('styleID')  # 风格类型

#         try:
#             user = self.db.query(User).filter(User.userID == m_sponsorID).one()
#             if user:  # 已注册
#                 appointment = Appointment(
#                     sponsorID=m_sponsorID,
#                     location=m_location,
#                     start_time=m_start_time,
#                     end_time=m_end_time,
#                     appointment_name=m_appointment_name,
#                     appointment_introduction=m_appointment_introduction,
#                     self_introduction=m_self_introduction,
#                     styleID=m_styleID,
#                     closed=False)
#                 if self.db.query(Appointment).filter(Appointment.sponsorID == m_sponsorID,
#                                                      Appointment.appointment_name == m_appointment_name,
#                                                      Appointment.appointment_introduction == m_appointment_introduction).all():
#                     retjson['content'] = '该活动已存在，请勿重复添加'
#                 else:
#                     self.db.merge(appointment)  # 在话题-用户表中加入改项
#                     try:
#                         self.db.commit()
#                         retjson['content'] = '添加活动成功'
#                     except:
#                         self.db.rollback()
#                         retjson['code'] = 408  # Request Timeout
#                         retjson['content'] = '该活动已存在！'
#         except:  # 未注册
#             retjson['code'] = 400
#             retjson['content'] = '请注册！'
#         self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # ensure_ascii:允许中文
#
#
# #
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
