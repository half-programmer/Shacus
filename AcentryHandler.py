# -*- coding:utf-8 -*-
__anthor__="wjl"
from BaseHandlerh import  BaseHandler
from Database.tables import ActivityEntry,User,Activity
from datetime import date, datetime
import json
import AcentryFunction
import AcFunction

class AskEntry(BaseHandler): #互动表相关操作
    retjson = {'code': 200, 'contents': 'none'}
    retdata = []  # list array
    def post(self):
        type=self.get_argument("type",default="null")
        if type=="10309": #查看已报名活动
            m_id=self.get_argument("registerid",default = "null")
            try:
                data=self.db.query(ActivityEntry).filter(ActivityEntry.ACEregisterid == m_id).all()
                for ID in data:
                     dataask = self.db.query(Activity).filter(Activity.ACid==ID.ACEacid).all()
                     for item in dataask:
                        AcFunction.response(item, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception,e:
                print e
                self.retjson['code']=10309
                self.retjson['contents']='no entry'
        elif type=='10310':
                m_ACEacid=self.get_argument("ACEacid",default="null")
                m_ACEregisterid=self.get_argument("ACEregisterid",default="null")
                m_comments=self.get_argument("ACEcomment",default="null")
                try:
                    data=self.db.query(ActivityEntry).filter(ActivityEntry.ACEacid==m_ACEacid and Activity.ACEregisterid==m_ACEregisterid).all()
                    for comm in data:
                       comm.ACEcomment=m_comments
                       self.db.commit()
                       AcentryFunction.response(comm,self.retdata)
                    self.retjson['contents']=self.retdata
                except:
                    self.retjson["code"]=10310
                    self.retdata["contents"]="no comments"



        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文



