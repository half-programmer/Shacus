# -*- coding: utf-8 -*-
import json

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

__author__ = 'huangxinchen'

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, AppointmentRegister, AppointmenmtEntry
import json
from datetime import date, datetime
import  AppointmentFunctions

class AskAppointment(BaseHandler):  # 对约拍的一系列请求
    retjson = {'code': 200, 'content': 'none'}
    retdata = []  # list array



    def post(self):
        type = self.get_argument('type', default='unsolved')  # 类型值

        if type == 'AskMyAppointments':  # 1.请求我发布的所有约拍
            userID = self.get_argument('userID', default='unsolved')
            try:
                data = self.db.query(Appointment).filter(Appointment.sponsorID == userID).all()
                AppointmentFunctions.response(data, self.retdata)
            except:
                self.retjson['code'] = 400
                self.retdata = 'no result found'

        elif type == 'AskAllAppointments':  # 2.请求所有约拍
            userID = self.get_argument('userID', default='unsolved')
            try:
                appointments = self.db.query(Appointment).all()  # 返回所有约拍
                AppointmentFunctions.response(appointments, self.retdata)
            except:
                self.retjson['code'] = 400
                self.retdata = 'no result found'
        elif type == 'AskOpenAppointments':  # 3.获得所有未关闭约拍
            userID = self.get_argument('userID', default='unsolved')
            try:
                appointments = self.db.query(Appointment).filter(Appointment.closed == False).all()  # 返回所有未关闭约拍
                AppointmentFunctions.response(appointments, self.retdata)
            except:
                self.retjson['code'] = 400
                self.retdata = 'no result found'
        elif type == 'AskParticipants':  # 4.获得某个约拍的所有报名者（包括自己的约拍）
            userID = self.get_argument('userID', default='unsolved')
            appointmentID = self.get_argument('appointmrntID', default='unsolved')  # 约拍ID
            try:
                registers = self.db.query(AppointmentRegister).filter(AppointmentRegister.appointmentID==appointmentID).all() # 某个约拍所有报名者
                for user in registers:
                    response = user.userID
                    AppointmentFunctions.response(response, self.retdata)
            except:
                self.retjson['code'] = 400
                self.retdata = 'no result found'



        self.retjson['content'] = self.retdata
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文
