# -*-coding: utf-8 -*-
from sqlalchemy import and_

__author__='lanwei'
import hashlib
import io
#from PIL import Image
import  json
from  Database.tables import User,Activity,ActivityParticipate
from  BaseHandlerh import BaseHandler
import commonFunctions
class  ActivityException(RuntimeError):
    def __init__(self,code,content):
        self.code=code
        self.content=content

class   ActivityCommit(BaseHandler):#创建活动
    def post(self):
        retjson={'code':200,'content':'ok'}#返回json
        try:
            #activityID自增
            m_sponsorID =self.get_argument('sponsorID',default=None)
            m_activity_name = self.get_argument('activity_name',default=None)
            m_activity_introduction = self.get_argument('activity_introduction',default=None)  # 活动介绍
            m_type = self.get_argument('type',default=None)  # 约拍类型
            m_location = self.get_argument('location',default=None)
            m_start_time = self.get_argument('start_time',default=None)
            m_end_time = self.get_argument('end_time',default=None)
            m_min_people = self.get_argument('min_people',default=None)
            m_max_people = self.get_argument('max_people',default=None)
            if not(m_start_time and m_end_time and m_location and m_activity_name and m_sponsorID):
                retjson['code']=300
                retjson['content']=u'信息不全'
            else:
               user = self.db.query(User).filter(User.userID == m_sponsorID).first()
               if user:
                   activity=Activity(
                       sponsorID=m_sponsorID,
                       activity_name=m_activity_name,
                       activity_introduction=m_activity_introduction,
                       type=m_type,
                       location=m_location,
                       start_time=m_start_time,
                       end_time=m_end_time,
                       min_people=m_min_people,
                       max_people=m_max_people,
                       closed=False,
                       imageurl=''
                   )
                   if self.db.query(Activity).filter(Activity.sponsorID==m_sponsorID).first():
                       raise ActivityException(402,u'该活动已存在,请勿重复添加')
                   else:
                       self.db.merge(activity)
                       retjson['content'] = u'发布活动成功'
                       commonFunctions.commit(self,retjson)
               else:
                   raise ActivityException(400,u'请注册')
        except ActivityException,e:
            retjson['code'] =e.code
            retjson['code']=e.content
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = u'系统错误！'

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # ensure_ascii:允许中文

class ActivityJoin(BaseHandler):
    def post(self):
        retjson = {'code': 200, 'content': 'ok'}
        m_userID=self.get_argument('userID',default='unsolved')#用户id
        m_activityID=self.get_argument("ActivityID",default='unsolved')#活动id
        try:
            activity=self.db.query(Activity).filter(Activity.activityID==m_activityID).one()
            if not activity.closed:
                data=self.db.query(ActivityParticipate).filter(and_(ActivityParticipate.activity_participateID==m_userID,
                                                                    ActivityParticipate.activityID==m_activityID)).first()#查询改用户是否已参加此活动
                if data:
                    retjson['code']=400
                    retjson['content']=u'不能重复报名'
                else:
                    actp=ActivityParticipate(
                        activity_participateID=m_userID,
                        activityID=m_activityID
                    )
                    self.db.merge(actp)  # 在用户_参加人员表用加入信息
                    retjson['content'] = u'参加活动成功'
                    commonFunctions.commit(self,retjson)
            else:
                retjson['code']=400
                retjson['content']=u'该活动已关闭'
        except:
            retjson['code']=400
            retjson['content']=u'该活动不存在'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # 在当前目录下生成retjson文件输出中文


