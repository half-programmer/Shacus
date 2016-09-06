# coding=utf-8
import json

from sqlalchemy import desc
from tornado import gen
from tornado.web import asynchronous

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User
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
                                headImage=r"http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg",
                                auth_key=u_auth_key
                            )
                            photo_list = []  # 摄影师发布的约拍
                            model_list = []
                            daohangl_list = []
                            daohangl_list.append(Model_daohanglan('data:image/jpeg;base64,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','http://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=%E7%BE%8E%E5%9B%BE&step_word=&hs=0&pn=1&spn=0&di=87339739080&pi=&rn=1&tn=baiduimagedetail&is=&istype=0&ie=utf-8&oe=utf-8&in=&cl=2&lm=-1&st=undefined&cs=1188453696%2C3651207681&os=3631960061%2C2297660335&simid=4175440435%2C726436141&adpicid=0&ln=1992&fr=&fmq=1472885603080_R&fm=&ic=undefined&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&ist=&jit=&cg=&bdtype=0&oriquery=&objurl=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F8cf76c63f6246b60d4f7bfafebf81a4c530fa26a.jpg&fromurl=ippr_z2C%24qAzdH3FAzdH3Fptjkw_z%26e3Bkwt17_z%26e3Bv54AzdH3FrAzdH3Fda08aln0aa&gsm=0&rpstart=0&rpnum=0'))
                            daohangl_list.append(
                                Model_daohanglan('http://image8.360doc.com/DownloadImg/2010/04/0412/2762690_45.jpg','http://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=%E7%BE%8E%E5%9B%BE&step_word=&hs=0&pn=24&spn=0&di=14293150190&pi=0&rn=1&tn=baiduimagedetail&is=&istype=0&ie=utf-8&oe=utf-8&in=&cl=2&lm=-1&st=undefined&cs=2860350365%2C3214019191&os=289517539%2C4157278886&simid=0%2C0&adpicid=0&ln=1992&fr=&fmq=1472885603080_R&fm=&ic=undefined&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&ist=&jit=&cg=&bdtype=0&oriquery=&objurl=http%3A%2F%2Fimage8.360doc.com%2FDownloadImg%2F2010%2F04%2F0412%2F2762690_45.jpg&fromurl=ippr_z2C%24qAzdH3FAzdH3Fooo_z%26e3Bnma15v_z%26e3Bv54AzdH3Fv5gpjgpAzdH3F8aAzdH3FabdaAzdH3F88AzdH3F8nad0dl_9098dc0d_z%26e3Bfip4s&gsm=0&rpstart=0&rpnum=0'))
                            try:
                                print 'shaixuanqian'

                                photo_list_all = self.db.query(Appointment).filter(Appointment.APtype == 1,
                                                                                   Appointment.APvalid == 1).\
                                    order_by(desc(Appointment.APcreateT)).limit(6).all()
                                model_list_all = self.db.query(Appointment).filter(Appointment.APtype == 0,
                                                                                   Appointment.APvalid == 1). \
                                    order_by(desc(Appointment.APcreateT)).limit(6).all()
                                from Appointment.APmodel import APmodelHandler
                                ap_model_handler = APmodelHandler()  # 创建对象
                                print 'chuangjianchengg'

                                ap_model_handler.ap_Model_simply(photo_list_all, photo_list, user.Uid)

                                ap_model_handler.ap_Model_simply(model_list_all, model_list, user.Uid)
                                print 'shaixuanchengg'
                                data = dict(
                                userModel=user_model,
                                daohanglan=daohangl_list,
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


