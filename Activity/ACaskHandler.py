#-*- coding:utf-8 -*-

'''
@王佳镭
@2016.9.3
'''
from sqlalchemy import desc

from BaseHandlerh import  BaseHandler
from Database.tables import Activity,User,ActivityImage
import json

import ACFunction
from BaseHandlerh import  BaseHandler
from Database.tables import Activity


class AskActivity(BaseHandler): #关于用户的一系列活动
    retjson = {'code': '', 'contents': 'none'}
    retdata = []  # list array
    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type == '10303':  # 1.查看所有活动
            try:
              #  data = self.db.query(Activity).all()
                data=self.db.query(Activity).order_by(desc(Activity.ACcreateT)).all()
                length=len(data)
                print length
                if length < 10:
                    for i in range(length):

                        #dataimage = self.db.query(ActivityImage).filter(data[i].ACid == ActivityImage.ACLacid).one()
                        ACFunction.Acresponse(data[i],self.retdata)
                        self.retjson['code']=10303
                        self.retjson['contents']=self.retdata
                else:
                    for item in range(0,10):
                            #dataimage = self.db.query(ActivityImage).filter(data[item].ACid == ActivityImage.ACLacid).one()
                            ACFunction.Acresponse(data[item],self.retdata)
                            self.retjson['code'] = 10303
                            self.retjson['contents'] = self.retdata
            except Exception, e:
                    print e
                    self.retjson['code'] = 200
                    self.retjson['contents'] = 'there is no activity'
        elif type =='10304':
            try:
                acsended=self.get_argument('acsended')
                Acsended=int(acsended)
                data= data=self.db.query(Activity).order_by(desc(Activity.ACcreateT)).all()
                length = len(data)
                print length
                m_length=length-Acsended
                print m_length
                if (m_length<5):
                    for i in range(Acsended,length):
                        #dataimage = self.db.query(ActivityImage).filter(data[i].ACid == ActivityImage.ACLacid).one()
                        ACFunction.Acresponse(data[i], self.retdata)
                        self.retjson['code'] = 10304
                        self.retjson['contents'] = self.retdata
                else:
                    for item in range(Acsended,acsended+6):
                        #dataimage = self.db.query(ActivityImage).filter(data[item].ACid == ActivityImage.ACLacid).one()
                        ACFunction.Acresponse(data[item],self.retdata)
                        self.retjson['code'] = 10304
                        self.retjson['contents'] = self.retdata

            except Exception,e:
                print e
                self.retjson['code'] = 200
                self.retjson['contents'] = 'there is no activity'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文
            # elif type=='10304':#查看活动详情
        #      m_ACid=self.get_argument("ACid",default="unknown")
        #      try:
        #         data=self.db.query(Activity).filter(m_ACid == Activity.ACid).all()
        #         for item in data:
        #             AcFunction.response(item,self.retdata)
        #         self.retjson['contents'] = self.retdata
        #      except Exception,e:
        #          print e
        #          self.retjson['code']=10304
        #          self.retjson['contents']='null information'

        #elif type=='10303':


       # self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

