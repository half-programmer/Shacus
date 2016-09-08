# coding=utf-8
import json

from sqlalchemy import desc
from tornado import gen
from tornado.web import asynchronous

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User
from Userinfo.Ufuncs import Ufuncs
from Userinfo.Usermodel import Model_daohanglan

class LoginHandler(BaseHandler):

    retjson = {'code': '', 'contents': u'未处理 '}

    @asynchronous
    @gen.coroutine
    def post(self):
        askcode = self.get_argument('askCode')  # 请求码
        m_phone = self.get_argument('phone')
        if askcode == '10106':  # 手动登录
            m_password = self.get_argument('password')
            if not m_phone or not m_password:
                self.retjson['code'] = 400
                self.retjson['contents'] = 10105  # '用户名密码不能为空'
        #todo:登录返回json的retdata多一层[]，客户端多0.5秒处理时间
        # 防止重复注册
            else:
                try:
                    user = self.db.query(User).filter(User.Utel == m_phone).one()
                    if user:  # 用户存在
                        password = user.Upassword
                        if m_password == password:  # 密码正确
                            print u'密码正确'
                            self.retjson['code'] = 200
                            if user.Ubirthday:
                                Ubirthday = user.Ubirthday.strftime('%Y-%m-%d %H:%M:%S'),
                            else:
                                Ubirthday = ''
                            retdata = []
                            u_auth_key = user.Uauthkey
                            user_model = dict(
                                id=user.Uid,
                                phone=user.Utel,
                                nickName=user.Ualais,
                                realName=user.Uname,
                                sign=user.Usign,
                                sex=user.Usex,
                                score=user.Uscore,
                                location=user.Ulocation,
                                birthday=Ubirthday,
                                registTime=user.UregistT.strftime('%Y-%m-%d %H:%M:%S'),
                                mailBox=user.Umailbox,
                                headImage=Ufuncs.get_user_headimage_intent_from_userid(user.Uid),
                                auth_key=u_auth_key,
                                chattoken=user.Uchattoken
                            )
                            photo_list = []  # 摄影师发布的约拍
                            model_list = []
                            try:
                                photo_list_all = self.db.query(Appointment).filter(Appointment.APtype == 1,
                                                                                   Appointment.APvalid == 1).\
                                    order_by(desc(Appointment.APcreateT)).limit(6).all()
                                model_list_all = self.db.query(Appointment).filter(Appointment.APtype == 0,
                                                                                   Appointment.APvalid == 1). \
                                    order_by(desc(Appointment.APcreateT)).limit(6).all()
                                from Appointment.APmodel import APmodelHandler
                                ap_model_handler = APmodelHandler()  # 创建对象

                                ap_model_handler.ap_Model_simply(photo_list_all, photo_list, user.Uid)
                                ap_model_handler.ap_Model_simply(model_list_all, model_list, user.Uid)
                                data = dict(
                                userModel=user_model,
                                daohanglan=self.bannerinit(),
                                photoList=photo_list,
                                modelList=model_list,
                                )
                                #todo 待生成真的导航栏

                                retdata.append(data)
                                self.retjson['code'] = '10101'
                                self.retjson['contents'] = retdata
                            except Exception,e:
                                print e
                                self.retjson['contents'] = r"摄影师约拍列表导入失败！"
                        else:
                            self.retjson['contents'] = u'密码错误'
                            self.retjson['code'] = '10104'  # 密码错误
                    else:  # 用户不存在
                        self.retjson['contents'] = u'该用户不存在'
                        self.retjson['code'] = '10103'
                except Exception, e:  # 还没有注册
                    print "异常："
                    print e
                    self.retjson['contents'] = u'该用户名不存在'
                    self.retjson['code'] = '10103' # '该用户名不存在'
        elif askcode == '10105':  # 自动登录
            authcode = self.get_argument("authcode")  # 授权码
        else:
            self.retjson['contents'] = u"登录类型不满足要求，请重新登录！"
            self.retjson['data'] = u"登录类型不满足要求，请重新登录！"
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.finish()

    def bannerinit(self):
        from FileHandler.Upload import AuthKeyHandler
        bannertokens = []

        authkeyhandler = AuthKeyHandler()
        banner1 = authkeyhandler.download_url("banner/banner1.jpg")
        banner2 = authkeyhandler.download_url("banner/banner2.jpg")
        banner3 = authkeyhandler.download_url("banner/banner3.jpg")
        banner4 = authkeyhandler.download_url("banner/banner4.jpg")
        banner_json1 = {'imgurl': banner1, 'weburl': "http://www.shacus.cn/"}
        banner_json2 = {'imgurl': banner2, 'weburl': "http://www.shacus.cn/"}
        banner_json3 = {'imgurl': banner3, 'weburl': "http://www.shacus.cn/"}
        banner_json4 = {'imgurl': banner4, 'weburl': "http://www.shacus.cn/"}
        bannertokens.append(banner_json1)
        bannertokens.append(banner_json2)
        bannertokens.append(banner_json3)
        bannertokens.append(banner_json4)
        return bannertokens

