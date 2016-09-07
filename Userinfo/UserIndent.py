# coding=utf-8

'''
@author   兰威
@type     用户订单
'''
import json

from Activity.ACmodel import ACmodelHandler
from Appointment.APmodel import APmodelHandler
from BaseHandlerh import BaseHandler
from Database.tables import ActivityEntry, Activity, AppointEntry, Appointment
from Userinfo import Ufuncs

class UserIndent(BaseHandler):
    retjson ={'code':'', 'contents':''}
    def post(self):
        ret_contents = {}
        ret_activity = []
        ret_e_appointment=[]
        ret_my_appointment=[]
        ac = ACmodelHandler()
        ap = APmodelHandler()
        type = self.get_argument('type')
        u_id = self.get_argument('uid')
        auth_key = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id,auth_key):
            if type == '10901':  # 查看我的已报名的约拍活动
                ret_activity =self.get_activity(u_id,0)
                ret_contents['activity'] = ret_activity
                ret_e_appointment =self.get_e_appointment(u_id,0)
                ret_contents['entryappointment'] = ret_e_appointment
                ret_my_appointment = self.get_my_appointment(u_id,0)
                ret_contents['myappointment'] = ret_my_appointment
                self.retjson['code'] = '10392'
                self.retjson['contents'] =ret_contents
            if type =='10902':    # 查看我的正在进行的约拍活动
                ret_activity = self.get_activity(u_id,1)
                ret_contents['activity'] =ret_activity
                ret_e_appointment = self.get_e_appointment(u_id, 1)
                ret_contents['entryappointment'] = ret_e_appointment
                ret_my_appointment = self.get_my_appointment(u_id, 1)
                ret_contents['myappointment'] = ret_my_appointment
                self.retjson['code'] = '10393'
                self.retjson['contents'] = ret_contents
            if type == '10903':    # 查看我的已经完成的约拍活动
                ret_activity = self.get_activity(u_id,2)
                ret_contents['activity'] =ret_activity
                ret_e_appointment = self.get_e_appointment(u_id, 2)
                ret_contents['entryappointment'] = ret_e_appointment
                ret_my_appointment = self.get_my_appointment(u_id, 2)
                ret_contents['myappointment'] = ret_my_appointment
                self.retjson['code'] = '10394'
                self.retjson['contents'] = ret_contents


        else :
            self.retjson['code'] = '10391'
            self.retjson['contents'] = '用户授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

    def get_activity(self,u_id,number):  #按照活动的状态和用户ID查看活动详情
        ret_activity=[]
        ac_enteys = self.db.query(ActivityEntry).filter(ActivityEntry.ACEregisterid == u_id,
                                                        ActivityEntry.ACEregisttvilid == True).all()

        for ac_entey in ac_enteys:
           ac_id = ac_entey.ACEacid
           ac_info = self.db.query(Activity).filter(Activity.ACid == ac_id,
                                                 Activity.ACstatus == number).all()
           if ac_info:
               ret_activity.append(ACmodelHandler.ac_Model_simply(ac_info[0]))
        return ret_activity


    def get_e_appointment(self,u_id,number):
        ret_e_appointment = []
        ap_e_info = []
        if number == 0:
           ap_e_entrys = self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == u_id,
                                                         AppointEntry.AEvalid == True).all()
        else :

            ap_e_entrys = self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == u_id,
                                                                 AppointEntry.AEvalid == True,
                                                                 AppointEntry.AEchoosed ==True).all()

        for ap_e_entry in ap_e_entrys:
            ap_id = ap_e_entry.AEapid
            try :
               ap_e_info = self.db.query(Appointment).filter(Appointment.APid == ap_id,Appointment.APstatus == number).all()
            except Exception,e:
                print e
            if ap_e_info:
                ret_e_appointment.append(APmodelHandler.ap_Model_simply_one(ap_e_info[0],u_id))
        return ret_e_appointment

    def get_my_appointment(self,u_id,number):
        ap_my_entrys = []
        ret_my_appointment =[]
        try:
            ap_my_entrys = self.db.query(Appointment).filter(Appointment.APsponsorid == u_id,Appointment.APstatus == number).all()
        except Exception,e:
            print e
        ret_my_appointment = APmodelHandler.ap_Model_simply(ap_my_entrys, ret_my_appointment,u_id)
        return ret_my_appointment

