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

    def ap_ask_user(self, uid):  # 查询指定用户的所有约拍
        '''
        :param user: 传入一个User对象
        :return: 无返回，直接修改retjson
        '''
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
                    print e
                    self.no_result_found(e)
            elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍中未关闭的
                retdata = []
                try:
                    appointments = self.db.query(Appointment). \
                        filter(Appointment.APtype == 0, Appointment.APstatus == 1, Appointment.APvalid == 1).all()
                    APmodelHandler.ap_Model_simply(appointments, retdata)
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.no_result_found(e)
            elif request_type == '10251':  # 返回约拍详情
                retdata = []
                ap_id = self.get_argument('apid')
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()
                    if appointment:
                        response = APmodelHandler.ap_Model_multiple(appointment)
                        print 'before equal'
                        try:
                            print "in try"
                            if appointment.APsponsorid == int(u_id):
                                response['AP_issponsor'] = 1
                            else:
                                response['AP_issponsor'] = 0
                        except Exception, e:
                            print e
                        self.retjson['code'] = '10250'
                        self.retjson['contents'] = response
                except Exception, e:
                    print e
                    self.no_result_found(e)
            elif request_type == '10240':
                self.ap_ask_user(u_id)

        else:
            self.retjson['contents'] = '授权码不存在或已过期'
            self.retjson['code'] = '10214'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

