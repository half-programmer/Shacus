# -*- coding:utf-8 -*-
import json
from  BaseHandlerh import BaseHandler
from Database.tables import User, UCinfo
from Database.tables import Verification
import random
from messsage import message

def generate_verification_code(len=6):
 ''' 随机生成6位的验证码 '''
 # 注意： 这里我们生成的是0-9的列表，当然你也可以指定这个list，这里很灵活
 code_list = []
 for i in range(10): # 0-9数字
  code_list.append(str(i))
 myslice = random.sample(code_list, len) # 从list中随机获取6个元素，作为一个片断返回
 verification_code = ''.join(myslice) # list to string
 return verification_code

def generate_auth_key(len=32):
   # 随机生成32位的验证码
   code_list = []
   for i in range(10):
       code_list.append(str(i))
   for i in range(65,91):
       code_list.append(chr(i))
   for i in range(97,123):
       code_list.append(chr(i))
   myslice = random.sample(code_list,len)
   auth_key=''.join(myslice)
   return  auth_key



class RegisterHandler(BaseHandler):
    print "进入regist"
    retjson = {'code': '400', 'contents': 'None'}
    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type == '10001':  # 验证手机号
            m_phone=self.get_argument('phone')
            try:
                user = self.db.query(User).filter(User.Utel == m_phone).one()
                if user:
                    self.retjson['contents'] = u"该手机号已经被注册，请更换手机号或直接登录"
                    self.retjson['code'] = 10005
            except:
                code=generate_verification_code()
                veri=Verification(
                    Vphone=m_phone,
                    Vcode=code,
                )
                self.db.merge(veri)
                try:
                    self.db.commit()
                    self.retjson['code'] = 10004 # success
                    self.retjson['contents'] = u'手机号验证成功，发送验证码'
                except:
                    self.db.rollback()
                    self.retjson['code'] = 10009  # Request Timeout
                    self.retjson['contents'] = u'服务器错误'
                message(code, m_phone)
        elif type=='10002': #验证验证码
            m_phone=self.get_argument('phone')
            code=self.get_argument('code')
            try:
               item=self.db.query(Verification).filter(Verification.Vphone==m_phone).one()
               if item.Vcode==code:
                   self.retjson['code']=10004
                   self.retjson['contents']=u'验证码验证成功'
               else:
                   self.retjson['code']=10006
                   self.retjson['contents']=u'验证码验证失败'
            except:
                self.retjson['code']=10007
                self.retjson['contents']=u'该手机号码未发送验证码'

        elif type=='10003': #注册详细信息
            m_password=self.get_argument('password')
            m_nick_name=self.get_argument('nickName')  # 昵称
            m_phone=self.get_argument('phone')
            m_auth_key=generate_auth_key()
            new_user=User(
                    Upassword=m_password,
                    Ualais=m_nick_name,
                    Uname='',
                    Ulocation='',  #  新用户注册默认level为1
                    Umailbox='',
                    Ubirthday='0000-00-00 00:00:00',
                    Utel=m_phone,
                    Uscore=0,
                    Usex=1,
                    Usign='',
                    Uauthkey=m_auth_key
            )
            try:
                same_nickname_user = self.db.query(User).filter(User.Ualais == m_nick_name).one()
                if same_nickname_user:  # 该昵称已被使用
                    self.retjson['code'] = 10008  # Request Timeout
                    self.retjson['contents'] =u'该昵称已被使用，请更换昵称'
            except: # 手机号和昵称皆没有被注册过
                    self.db.merge(new_user)
                    try:
                        self.db.commit()
                        self.retjson['code'] = 10004  # success
                        m_time = self.db.query(User.UregistT).filter(User.Uauthkey == m_auth_key).one()
                        m_id = self.db.query(User.Uid).filter(User.Uauthkey == m_auth_key).one()
                        retdata = []
                        retdata_body = {}
                        data=dict(
                            phone = m_phone,
                            authkey  = m_auth_key,
                            nickName = m_nick_name,
                            headImage ='',
                            realName ='',
                            birthday ='',
                            sign ='',
                            score ='',
                            location ='',
                            registTime ='',
                            mailbaox = '',
                            id = m_id[0]
                        )
                        retdata_body['userModel'] =data
                        retdata.append(retdata_body)
                        try:
                            u_info = UCinfo(
                                UCuid = m_id[0],
                                UClikeN=0,
                                UClikedN=0,
                                UCapN=0,
                                UCphotoN=0,
                                UCcourseN=0,
                                UCmomentN=0
                            )
                            self.db.merge(u_info)
                            self.db.commit()
                        except Exception, e:
                            print e
                            self.retjson['contents'] =r'初始化用户信息时出错'  # ucinfo插入失败
                        self.retjson['contents'] = retdata

                    except Exception, e:
                        print e
                        self.db.rollback()
                        self.retjson['code'] = 10009  # Request Timeout
                        self.retjson['contents'] = u'Some errors when commit to database, please try again'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

