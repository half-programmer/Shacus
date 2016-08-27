# coding=utf-8
import json
from  BaseHandlerh import BaseHandler
from Database.tables import Appointment,User
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

class RegisterHandler(BaseHandler):
    retjson = {'code': '400', 'contents': 'None'}
    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type == '10001':  # 验证手机号
            m_phone=self.get_argument('phone')
            try:
                user = self.db.query(User).filter(User.phone == m_phone).one()
                if user:
                    self.retjson['content'] = u"该手机号已经被注册，请更换手机号或直接登录"
                    self.retjson['code'] = 10005
            except:
                code=generate_verification_code()
                veri=Verification(
                    phone=m_phone,
                    verificationcode=code
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
               item=self.db.query(Verification).filter(Verification.phone==m_phone).one()
               if item.verificationcode==code:
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
            new_user=User(
                    password=m_password,
                    nick_name=m_nick_name,
                    real_name='',
                    level=1,  #  新用户注册默认level为1
                    location='',
                    birthday='',
                    phone=m_phone,
                    regist_time=''
            )
            try:
                same_nickname_user = self.db.query(User).filter(User.nick_name == m_nick_name).one()
                if same_nickname_user:  # 该昵称已被使用
                    self.retjson['code'] = 10008  # Request Timeout
                    self.retjson['contents'] =u'该昵称已被使用，请更换昵称'
            except: # 手机号和昵称皆没有被注册过
                    self.db.merge(new_user)
                    try:
                        self.db.commit()
                        self.retjson['code'] = 10004  # success
                        self.retjson['contents'] = u'注册成功'
                    except:
                        self.db.rollback()
                        self.retjson['code'] = 10009  # Request Timeout
                        self.retjson['contents'] = u'Some errors when commit to database, please try again'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

