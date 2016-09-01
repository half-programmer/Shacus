#-*- coding:utf-8 -*-
__anthor__="wjl"
from BaseHandlerh import  BaseHandler
from Database.tables import Activity,User
import json
from datetime import date, datetime
import ACFunction

class AskActivity(BaseHandler): #关于用户的一系列活动
    retjson = {'code': 200, 'contents': 'none'}
    retdata = []  # list array
    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type == '10303':  # 1.查看所有活动
            try:
                data = self.db.query(Activity).all()
                for item in (0 ,10):
                    ACFunction.response(data[item], self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception, e:
                print e
                self.retjson['code'] = 10303
                self.retjson['contents'] = 'there is no activity'

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


        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文


