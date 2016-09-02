# coding=utf-8
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, UserImage, UCinfo


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






    retjson = {'code':'','contents':''}
    retdata = []
    ret_json_contents = {}

    def post(self):

        # todo 还未增加图片地址,活动按时间排序


        u_id = self.get_argument('uid')
        auth_key = self.get_argument('authkey')
        if self.judge_user_valid(u_id,auth_key):
            u_info = self.db.query(User).filter(User.Uid == u_id).one()
            #u_image_info = self.db.query(UserImage).filter(UserImage.UIuid == u_id).one()
            u_change_info =self.db.query(UCinfo).filter(UCinfo.UCuid == u_id).one()
            ret_user_info = {'uid':u_info.Uid,'ualais':u_info.Ualais,'ulocation':u_info.Ulocation,
                       'utel':u_info.Utel,'uname':u_info.Uname,'umailbox':u_info.Umailbox,
                       'ubirthday':u_info.Ubirthday,'uscore':u_info.Uscore,'usex':u_info.Usex,
                       'usign':u_info.Usign,'uimage':'','ulikeN':u_change_info.UClikeN,
                       'ulikedN':u_change_info.UClikedN,'uapN':u_change_info.UCapN,
                       'uphotoN':u_change_info.UCphotoN,'ucourseN':u_change_info.UCcourseN,
                       'umomentN':u_change_info.UCmomentN}
            #self.retjson['contents'] = retdata
            self.retjson['code'] = '10501'
        else:
            self.retjson['code'] = '10500'
            self.retjson['contents'] ='授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))


