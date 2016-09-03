# coding=utf-8
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, UserImage, UCinfo, Appointment, UserLike, AppointmentInfo,AppointEntry, ActivityEntry, \
    Activity
from Appointment.APmodel import user_ap_simply
from ACmodel import user_ac_simply
from Userinfo.Usermodel import userinfo_smply
class Userhomepager(BaseHandler):


    def get_user_id(self, u_auth_key):
        '''
        通过用户auth_key获得id
        :param u_auth_key:
        :return: 成功则返回id,失败返回0
        '''
        try:
            user = self.db.query(User).filter(User.Uauthkey == u_auth_key).one()
            uid = user.Uid
            return uid
        except Exception, e:
            return 0

    def get_user_authkey(self, u_id):
        '''
        @attention: 直接调用时需要判断是否为0,返回0则该用户不存在
        :param u_id:
        :return:用户存在则返回u_auth_key，否则返回0
        '''
        try:
            user = self.db.query(User).filter(User.Uid == u_id).one()
            if user:
                u_auth_key = user.Uauthkey
                return u_auth_key
        except Exception, e:
            print 'edsdsd:::', e
            return 0

    def judge_user_valid(self, uid, u_authkey):
        # todo:可以完善区别是不合法还是用户不存在，以防止攻击
        '''
        判断用户是否合法
        :return:合法返回1，不合法返回0
        '''
        try:
            u_id = self.get_user_id(u_authkey)
            if u_id == int(uid):
                return 1  # 合法
            else:
                print 'shdasidasd'
                return 0  # 不合法
        except Exception, e:
            print e
            return 0








    def post(self):

        # todo 还未增加图片地址,活动按时间排序
        retjson = {'code': '', 'contents': ''}
        retdata_ap = []
        ret_json_contents = {}
        retdata_ac = []


        u_id = self.get_argument('uid')
        auth_key = self.get_argument('authkey')
        u_other_id = self.get_argument('seeid')
        if self.judge_user_valid(u_id,auth_key):
            u_info = self.db.query(User).filter(User.Uid == u_other_id).one()
            #u_image_info = self.db.query(UserImage).filter(UserImage.UIuid == u_other_id).one()
            u_change_info =self.db.query(UCinfo).filter(UCinfo.UCuid == u_other_id).one()
            ret_user_info = userinfo_smply(u_info,u_change_info)
            ret_json_contents['user_info'] = ret_user_info
            exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,UserLike.ULlikedid == u_other_id,
                                                   UserLike.ULvalid ==1).all()
            if exist :
                ret_json_contents['follow'] =True
            else:
                ret_json_contents['follow'] = False
            u_appointment_infos = self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == u_other_id,
                                                                     AppointEntry.AEvalid ==1).all()
            for u_appointment_info in u_appointment_infos:
                ap_id = u_appointment_info.AEapid
                try:
                    ap_info = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()
                    ret_ap = user_ap_simply(ap_info)
                    retdata_ap.append(ret_ap)
                except Exception,e:
                    print e
                    retjson['code'] = '10602'
                    retjson['contents']='该约拍不存在'
            u_spap_infos = self.db.query(Appointment).filter(Appointment.APsponsorid == u_other_id).all()
            for u_spap_info in u_spap_infos:
                ret_ap = user_ap_simply(u_spap_info)
                retdata_ap.append(ret_ap)
            ret_json_contents['ap_info'] =retdata_ap
            u_ac_infos = self.db.query(ActivityEntry).filter(ActivityEntry.ACEregisterid == u_other_id,
                                                             ActivityEntry.ACEregisttvilid ==1).all()
            for u_ac_info in u_ac_infos:
                ac_id = u_ac_info.ACEacid
                ac_info = self.db.query(Activity).filter(Activity.ACid ==ac_id ).one()
                ret_ac  = user_ac_simply(ac_info)
                retdata_ac.append(ret_ac)
            ret_json_contents['ac_info'] =retdata_ac
            retjson['code'] = '10601'
            retjson['contents'] =ret_json_contents

        else:
            retjson['code'] = '10600'
            retjson['contents'] ='授权码不正确'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))


