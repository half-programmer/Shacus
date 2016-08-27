# coding=utf-8
import json
import commonFunctions
from  BaseHandlerh import BaseHandler
from Database.tables import Appointment, User, AppointmentRegister, AppointmenmtEntry


class CreateAppointment(BaseHandler):  # 创建约拍
    def post(self):
        m_sponsorID = self.get_argument('sponsorID')  # 发起人
        m_location = self.get_argument('location')  # 位置
        m_start_time = self.get_argument('startTime')
        m_end_time = self.get_argument('endTime')
        m_appointment_name = self.get_argument('appointmentName')
        m_appointment_introduction = self.get_argument('appointmentIntroduction')
        m_self_introduction = self.get_argument('selfIntroduction')  # 自我介绍
        m_styleID = self.get_argument('styleID')  # 风格类型
        retjson = {'code': '400', 'content': 'None'}
        try:
            user = self.db.query(User).filter(User.userID == m_sponsorID).one()
            if user:  # 已注册
                appointment = Appointment(
                    sponsorID=m_sponsorID,
                    location=m_location,
                    start_time=m_start_time,
                    end_time=m_end_time,
                    appointment_name=m_appointment_name,
                    appointment_introduction=m_appointment_introduction,
                    self_introduction=m_self_introduction,
                    styleID=m_styleID,
                    closed=False)
                if self.db.query(Appointment).filter(Appointment.sponsorID == m_sponsorID,
                                                     Appointment.appointment_name == m_appointment_name,
                                                     Appointment.appointment_introduction == m_appointment_introduction).all():
                    retjson['content'] = '该活动已存在，请勿重复添加'
                else:
                    self.db.merge(appointment)  # 在话题-用户表中加入改项
                    try:
                        self.db.commit()
                        retjson['content'] = '添加活动成功'
                    except:
                        self.db.rollback()
                        retjson['code'] = 408  # Request Timeout
                        retjson['content'] = '该活动已存在！'
        except:  # 未注册
            retjson['code'] = 400
            retjson['content'] = '请注册！'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # ensure_ascii:允许中文


#
class RegistAppointment(BaseHandler):  # 报名约拍
    def post(self):
        m_user = self.get_argument('userID', default='unsolved')
        m_appointment_number = self.get_argument('appointmentID', default='unsolved')  # 想报名的活动
        retjson = {'code': '400', 'content': 'None'}
        try:
            appointment = self.db.query(Appointment).filter(Appointment.appointmentID == m_appointment_number).one()
            if not appointment.closed:  # 活动未关闭
                if m_user != appointment.sponsorID:  # 不是发布人
                    try:
                        if self.db.query(AppointmentRegister).filter(
                                        AppointmentRegister.appointmentID == m_appointment_number,
                                        AppointmentRegister.registerID == m_user).one():  # 已经报过名
                            retjson['content'] = '不能重复报名'
                    except:
                        new_register = AppointmentRegister(
                            appointmentID=m_appointment_number,
                            registerID=m_user
                        )
                        self.db.merge(new_register)  # 在报名人中加入该项
                        retjson['code'] = 200
                        retjson['content'] = '报名成功'
                        commonFunctions.commit(self, retjson)  # 提交
                else:
                    retjson['code'] = 400
                    retjson['content'] = '不能报名自己发布的活动'
            else:
                retjson['code'] = 400
                retjson['content'] = '该活动已关闭'
        except:
            retjson['code'] = 400
            retjson['content'] = '该活动不存在或未登陆'

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # ensure_ascii:允许中文


        # self.db.query(Appointment).filter(Appointment.appointmentID == m_appointment_number).update({"closed": True})  #
