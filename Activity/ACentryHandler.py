# -*- coding:utf-8 -*-
import datetime

__anthor__="wjl"
import json

import ACFunction
import ACentryFunction
from BaseHandlerh import  BaseHandler
from Database.tables import ActivityEntry, Activity,ActivityLike


class AskEntry(BaseHandler): #活动报名点赞表相关操作
    retjson = {'code': 200, 'contents': 'none'}
    retdata = []  # list array
    def post(self):
        type=self.get_argument("type",default="null")
        if type=="10309": #查看已报名活动
            m_id=self.get_argument("registerid",default = "null")
            try:
                data=self.db.query(ActivityEntry).filter(ActivityEntry.ACEregisterid == m_id).all()
                for ID in data:
                     dataask = self.db.query(Activity).filter(Activity.ACid == ID.ACEacid).all()
                     for item in dataask:
                        ACFunction.response(item, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception,e:
                print e
                self.retjson['code']=10309
                self.retjson['contents']='page failed'
        elif type=='10308':      #评价活动
                m_ACEacid=self.get_argument("ACEacid",default="null")
                m_ACEregisterid=self.get_argument("ACEregisterid",default="null")
                m_comments=self.get_argument("ACEcomment",default="null")
                try:

                    data=self.db.query(ActivityEntry).filter(ActivityEntry.ACEacid==m_ACEacid, ActivityEntry.ACEregisterid==m_ACEregisterid).one()
                    if not data.ACEcomment:
                        data.ACEcomment=m_comments
                        self.db.commit()
                        ACentryFunction.response(data, self.retdata)
                        self.retjson['code'] = '10381'
                        self.retjson['contents'] = "评论成功"
                    else:
                        self.retjson['contents']='评论已经存在'
                        self.retjson['code']='10383'

                except Exception,e:

                    print e
                    self.retjson["code"]='10382'

                    self.retjson["contents"]="no comments"
        elif type=='10311':#活动点赞
            m_ACLacid=self.get_argument("ACLacid",default="null")
            m_ACLudi=self.get_argument("ACLuid",default='null')
            try:
                data=self.db.query(ActivityLike).filter(Activity.ACLacid==m_ACLacid,ActivityLike.ACLuid==m_ACLudi,ActivityLike.ACLvalid==False).one()
            # if data:
            #     self.retdata['contents']='你已经点赞过此'
                new_ACLide=ActivityLike(
                   ACLacid=m_ACLacid,
                    ACLuid=m_ACLudi,
                    AClvalid=1,
                    )
                self.db.merge(new_ACLide)
                self.db.commit()
                self.retjson['code'] = '10311'
                self.retjson['contents'] = '点赞成功'
            except Exception,e:
                print e
                self.retjson['code']=10312
                self.retjson['contents']='点赞未成功'
        elif type=='10313':
            m_ACLacid = self.get_argument("ACLacid", default="null")
            m_ACLudi = self.get_argument("ACLuid", default='null')
            try:
                data = self.db.query(ActivityLike).filter(Activity.ACLacid == m_ACLacid, ActivityLike.ACLuid == m_ACLudi,ActivityLike.ACLvalid == True).one()
                data.ACLvalid = False
                self.retjson['code'] = '10313'
                self.retjson['contents'] = '取消点赞成功'
            except Exception,e:
                print e
                self.retjson['code']='10314'
                self.retjson['contents']='取消点赞失败'








        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文



