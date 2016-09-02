# coding=utf-8
import json

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User


class LoginHandler(BaseHandler):

    retjson = {'code': '', 'contents': u'未处理 '}
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
                                headImage=u"用户头像url",
                                auth_key=u_auth_key
                            )
                            photo_list = []  # 摄影师发布的约拍
                            model_list = []
                            try:
                                print 'shaixuanqian'

                                photo_list_all = self.db.query(Appointment).filter(Appointment.APtype == 1,
                                                                                   Appointment.APvalid == 1).all()
                                model_list_all = self.db.query(Appointment).filter(Appointment.APtype == 0,
                                                                                   Appointment.APvalid == 1).all()
                                from Appointment.APmodel import APmodelHandler
                                ap_model_handler = APmodelHandler()  # 创建对象
                                print 'chuangjianchengg'
                                for photo_list_each in photo_list_all:
                                    photo_list.append(ap_model_handler.ap_Model_simply(photo_list_each))
                                for model_list__each in model_list_all:
                                    model_list.append(ap_model_handler.ap_Model_simply(model_list__each))
                                print 'shaixuanchengg'
                                data = dict(
                                userModel=user_model,
                                daohanglan=u"约拍首页顶部滑动图片,应设置与本地对比或增加一特定链接，图片未更新时应使用本地缓存",
                                photoList=photo_list,
                                modelList=model_list,
                                )
                                retdata.append(data)
                                self.retjson['code'] = '10101'
                                self.retjson['contents'] = retdata
                            except Exception,e:
                                print e
                                self.retjson['contents'] = r"摄影师约拍列表导入失败！"

                        else:
                            self.retjson['contents'] = u'密码错误'
                            self.retjson['code'] = 10104  # 密码错误
                    else:  # 用户不存在
                        self.retjson['contents'] = u'该用户不存在'
                        self.retjson['code'] = 10103
                except Exception, e:  # 还没有注册
                    print "异常："
                    print e
                    self.retjson['contents'] = u'该用户名不存在'
                    self.retjson['code'] = 10103 # '该用户名不存在'
        elif askcode == '10105':  # 自动登录
            authcode = self.get_argument("authcode")  # 授权码
        else:
            self.retjson['contents'] = u"登录类型不满足要求，请重新登录！"
            self.retjson['data'] = u"登录类型不满足要求，请重新登录！"
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))



