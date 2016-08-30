# coding=utf-8
import json

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User


class LoginHandler(BaseHandler):

    retjson = {'code': '400', 'contents': u'未处理 ', 'Code': ''}
    def post(self):
        askcode = self.get_argument('askCode')  # 请求码
        m_phone = self.get_argument('phone')
        if askcode == '10106':  # 手动登录
            m_password = self.get_argument('password')
            if not m_phone or not m_password:
                self.retjson['code'] = 400
                self.retjson['contents'] = 10105  # '用户名密码不能为空'

        # 防止重复注册
            else:
                try:
                    user = self.db.query(User).filter(User.Utel == m_phone).one()
                    if user:  # 用户存在
                        password = user.Upassword
                        if m_password == password:  # 密码正确
                            self.retjson['code'] = 200
                            if user.Ubirthday:
                                Ubirthday = user.Ubirthday.strftime('%Y-%m-%dT%H:%M:%S'),
                            else:
                                Ubirthday = ''
                            retdata = []
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
                                registTime=user.UregistT.strftime('%Y-%m-%dT%H:%M:%S'),
                                mailBox=user.Umailbox,
                            )
                            data = dict(
                            askCode="10106",
                            authKey="待生成",
                            userModer=user_model,
                            daohanglan="约拍首页顶部滑动图片,应设置与本地对比或增加一特定链接，图片未更新时应使用本地缓存",
                            photoList="摄影师榜前十名,每人是一组数据,用python字典存,返回后可用JSON解析",
                            modelList="模特榜前十名，每人是一组数据,用python字典存,返回后可用JSON解析",
                            headImage="用户头像url"
                            )
                            retdata.append(data)
                            self.retjson['Code'] = 10101
                            self.retjson['contents'] = retdata

                        else:
                            self.retjson['Code'] = 10104  # 密码错误
                    else:  # 用户不存在
                        self.retjson['Code'] = 10103
                except Exception, e:  # 还没有注册
                    print "异常："
                    print e
                    self.retjson['code'] = 400
                    self.retjson['Code'] = 10103 # '该用户名不存在'
        elif askcode == '10105':  # 自动登录
            authcode = self.get_argument("authcode")  # 授权码
        else:
            self.retjson['data'] = u"登录类型不满足要求，请重新登录！"
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))



