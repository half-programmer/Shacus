# coding=utf-8
'''
  黄鑫晨,王佳镭
  2016.08.29

'''
import json
import types
from operator import and_

import AppFuncs
import ApInfoFuncion
from FileHandler.Upload import AuthKeyHandler
from  BaseHandlerh import BaseHandler

from Database.tables import Appointment, User, Verification,AppointmentInfo,AppointEntry

from AppFuncs import response



class APcreateHandler(BaseHandler):  # 创建约拍
    retjson = {'code': '', 'contents': 'None'}

    def post(self):
        # 10201 客户端请求，摄影师发布约拍  start

        ap_type = self.get_argument('type')
        if ap_type == '10201' or ap_type == '10202':  # 请求获得上传权限
            print '进入10201'
            user_phone = self.get_argument('phone')
            auth_key = self.get_argument('auth_key')
            ap_title = self.get_argument('title')
            ap_imgs = self.get_argument('imgs')
            print '获得图片'
            try:
                sponsor = self.db.query(User).filter(User.Utel == user_phone).one()
                print '进入try::::::'
                key = sponsor.Uauthkey
                ap_sponsorid = sponsor.Uid
                print  'ap_sponsorid::::',ap_sponsorid
                print 'ap_title::::',ap_title
                if auth_key == key:  # 认证成功
                    print '认证成功'
                    try:
                        appointment = self.db.query(Appointment).filter(Appointment.APtitle == ap_title).one()
                        if appointment:
                            self.retjson['code'] = '10210'
                            self.retjson['contents'] = r'该约拍已存在'
                    except Exception, e:
                        print e
                        retjson_body = {'auth_key': '', 'apId': ''}
                        auth_key_handler = AuthKeyHandler()
                        ap_imgs_json = json.loads(ap_imgs)
                        retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)
                        self.retjson['code'] = 10200
                        aptype = int(ap_type) - 10201

                        new_appointment = Appointment(
                            APtitle=ap_title,
                            APsponsorid=sponsor.Uid,
                            APtype=int(ap_type)-10201,
                            APlocation='',
                            APstartT='0000-00-00:00:00:00',
                            APendT='0000-00-00:00:00:00',
                            APcontent='',  # 活动介绍
                            APclosed=0,
                            APlikeN=0,
                            APvalid=1,
                            APaddallowed=0
                        )
                        self.db.merge(new_appointment)
                        self.db.commit()
                        try:
                            print '插入成功，进入查询'
                            ap = self.db.query(Appointment).filter(
                                   Appointment.APtitle == ap_title, Appointment.APsponsorid == ap_sponsorid).one()
                            ap_id = ap.APid
                            retjson_body['apId'] = ap_id
                            self.retjson['contents'] = retjson_body
                        except Exception,e:
                            print '插入失败！！'
                            self.retjson['contents'] = r'服务器插入失败'
                else:
                    self.retjson['code'] = '10211'
                    self.retjson['contents'] = r'用户授权码错误'
            except Exception, e:
                print e
                self.retjson['code'] = '10212'
                self.retjson['contents'] = "该用户名不存在"
        elif ap_type == '10205':  # 开始传输数据
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
                user = self.db.query(User.Uid).filter(User.Uauthkey == auth_key).one()  # 查看该用户id
                uid = user.Uid
                print 'uid: ', uid
                print '找到用户id'
                try:
                    print '判断该活动是否已经存在'
                    exist = self.db.query(Appointment).filter(Appointment.APtype == ap_type,
                                                              Appointment.APtitle == ap_title,
                                                              Appointment.APsponsorid == uid
                                                              ).one()  # 判断该活动是否已经存在
                    if exist:
                        print '活动存在'
                        self.retjson['code'] = '10210'
                        self.retjson['contents'] = '该约拍已存在'
                except Exception, e:
                    print e
                    try:
                        exist = self.db.query(Appointment).filter(Appointment.APid == ap_id,
                                                                  Appointment.APtitle == ap_title
                                                                  ).one()
                        print '判断授权是否存在'
                        if exist:
                            ap_sponsorid = exist.APsponsorid
                            if uid == ap_sponsorid:
                                print '授权存在'
                                self.db.query(Appointment).filter(Appointment.APid == ap_id). \
                                    update({Appointment.APstartT: ap_start_time, Appointment.APendT: ap_end_time,
                                            Appointment.APjoinT: ap_join_time,
                                            Appointment.APlocation: ap_location, Appointment.APfree: ap_free,
                                            Appointment.APcontent: ap_content,
                                            Appointment.APaddallowed: ap_addallowed,
                                            Appointment.APtype: ap_type
                                            }, synchronize_session=False)
                                self.db.commit()
                                self.retjson['code'] = '10214'
                                self.retjson['contents'] = '发布约拍成功'
                            else:
                                print 'fd'
                    except Exception, e:
                        print e
                        self.retjson['code'] = '10213'
                        self.retjson['contents'] = r'该发布尚未获得权限！'
            except Exception, e:
                print e
                self.retjson['code'] = '10211'
                self.retjson['contents'] = r'用户授权码错误！'
        else:
            print 'ap_type: ', ap_type
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

        # 判断返回是否许可

        # 10201 客户端请求，摄影师发布约拍 end


class APregistHandler(BaseHandler):  # 报名约拍
    retjson = {'code': '', 'contents': ''}

    def post(self):
        ap_registe_type = self.get_argument('type')
        if ap_registe_type == '10251':
            auth_key = self.get_argument('auth_key')
            ap_id = self.get_argument('apid')
            try:
                ap_user = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                ap_user_id = ap_user.Uid
                try :
                    exist = self.db.query(AppointEntry).\
                    filter(AppointEntry.AEregisterID == ap_user_id and AppointEntry.AEapid == ap_id).one() # 应该再加上和ap_id的验证
                    if exist:
                        self.retjson['contents'] = '已报名过该约拍'
                        self.retjson['code'] = '10250'
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
                        self.retjson['code'] = '10253'
                    except Exception,e:
                        print e
                        self.rollback()
                        self.retjson['contents'] = '数据库插入错误'
                        self.retjson['code'] = '10254'
            except Exception,e:
                print e
                self.retjson['contents'] = '授权码不存在或已过期'
                self.retjson['code'] = '10214'
        if ap_registe_type == '10252': #用户取消报名
            auth_key = self.get_argument('authkey')
            ap_id = self.get_argument('apid')
            try:
                ap_user = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                ap_user_id = ap_user.Uid
                try:
                    exist = self.db.query(AppointEntry).filter(
                        AppointEntry.AEregisterID == ap_user_id and AppointEntry.AEapid == ap_id).one()  # 应该再加上和ap_id的验证
                    if exist.AEvalid:
                        self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == ap_user_id).\
                            updata({AppointEntry.AEvalid == 0})
                        try :
                            self.db.commit()
                            self.retjson['contents'] = '取消报名成功'
                            self.retjson['code'] = '10255'
                        except Exception,e:
                            print e
                            self.rollback()
                            self.retjson['contents'] = '数据库更新错误'
                            self.retjson['code'] = '10254'
                    else :
                        self.retjson['contents'] = '用户已经取消报名'
                        self.retjson['code'] = '10256'
                except Exception, e:
                    self.retjson['contents'] = '用户未报名过该约拍'
                    self.retjson['code'] = '10257'
            except Exception, e:
                print e
                self.retjson['contents'] = '授权码不存在或已过期'
                self.retjson['code'] = '10214'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))





class APaskHandler(BaseHandler):  # 请求约拍相关信息

    # todo:返回特定条件下的约拍
    retjson = {'code': '', 'contents': ''}
    retdata = []

    def no_result_found(self, e):
        print e
        self.retjson['code'] = 400
        self.retdata = 'no result found'

    def ap_ask_user(self, user):  # 查询指定用户的所有约拍
        '''
        :param user: 传入一个User对象
        :return: 无返回，直接修改retjson
        '''
        uid = user.Uid
        try:
            appointments = self.db.query(Appointment).filter(Appointment.APsponsorid == uid).all()
            AppFuncs.response(appointments, self.retdata)
            self.retjson['contents'] = self.retdata
        except Exception, e:
            self.no_result_found(e)

    def post(self):
        auth_key = self.get_argument('authkey')
        request_type = self.get_argument('type')
        if request_type == '10231':  # 请求所有设定地点的摄影师发布的约拍中未关闭的
            try:
                appointments = self.db.query(Appointment). \
                    filter(Appointment.APtype == 1, Appointment.APclosed == 0).all()
                AppFuncs.response(appointments, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception, e:
                self.no_result_found(e)
        elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍中未关闭的
            try:
                appointments = self.db.query(Appointment). \
                    filter(Appointment.APtype == 2, Appointment.APclosed == 0).all()
                AppFuncs.response(appointments, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception, e:
                self.no_result_found(e)
        elif request_type == '10240':  # 请求用户自己发布的所有约拍
            try:
                user = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                self.ap_ask_user(user)
            except Exception, e:
                self.retjson['contents'] = '授权码不存在或已过期'
                self.retjson['code'] = '10214'
        elif request_type == '10241':  # 请求指定用户发布的所有约拍
            uid = self.get_argument('uid')  # 指定用户的id
            try:
                user = self.db.query(User).filter(User.Uid == uid).one()
                self.ap_ask_user(user)
            except Exception, e:
                self.retjson['contents'] = '授权码不存在或已过期'
                self.retjson['code'] = '10214'

        elif request_type == '10270':#在报名约拍中的人里选择约拍对象
           # uid = self.get_argument("uid",default="none")

            m_AEapid=self.get_argument("AEapid",default="null")
            try:
                data=self.db.query(AppointEntry).filter(AppointEntry.AEapid==m_AEapid  and AppointEntry.AEvalid==1).all()
                for item in data:
                    ApInfo=self.db.query(User).filter(User.Uid==item.AEregisterID).all()
                    for data in ApInfo:
                        ApInfoFuncion.ApUserinfo(data ,self.retdata)
                        self.retjson['code']='success'
                        self.retjson['contents']= self.retdata
            except Exception, e:
                    print e
                    self.retjson['contents']='选择约拍对象失败'
                    self.retdata['code']='10270'
        elif request_type == '10271':
           # choose = True
            m_APid=self.get_argument("APid",default="null")
            m_AEregisterid=self.get_argument("AEregisterid",default="null")
            m =int(m_AEregisterid)
            try:
                #data=self.db.query(AppointEntry).filter(AppointEntry.AEapid == m_APid and AppointEntry.AEregisterID == m_AEregisterid).one()
                data=self.db.query(AppointEntry).filter(AppointEntry.AEapid == m_APid and AppointEntry.AEregisterID == m).one()
                data.AEchoosed = True
                self.db.commit()
                self.retjson["code"]="10271"
                self.retjson["contents"]="选择成功！"
            except Exception, e:
                print e
                self.retjson['contents'] = '选择约拍对象失败'
                self.retdata['code'] = '10271'

        elif request_type =='10261':   #查看自己报名的约拍的结果
            uid = self.get_argument('uid')
            ap_id = self.get_argument('apid')
            try:
                u_result = self.db.query(AppointEntry.AEchoosed).\
                    filter(AppointEntry.AEapid ==ap_id and AppointEntry.AEregisterID == uid).one()
                self.retjson['code'] = '10263'
                self.retjson['contents'] = u_result[0]
            except Exception,e:
                print e
                self.retjson['code'] = '10262'
                self.retjson['contents'] = '用户未参加此约拍的报名'





        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

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

# class APregietHandler(BaseHandler):  # 报名约拍
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
#         # self.db.query(Appointment).filter(Appointment.appointmentID == m_appointment_number).update({"closed": True})  #
