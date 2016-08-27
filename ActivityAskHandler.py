# -*- coding: utf-8 -*-
import json

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

__author__ ='lanwei'

from BaseHandlerh import  BaseHandler
from Database.tables import Activity,ActivityParticipate,User
import json
from datetime import date, datetime
import ActivityFuction


class AskActivity(BaseHandler): #对活动的一系列请求
    retjson = {'code': 200, 'content': 'none'}
    retdata = []  # list array

    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type=='AskMyActivity':#1.请求我发布的所有活动
            m_userID=self.get_argument('userID',default='unsolved')
            try:
               data=self.db.query(Activity).filter(Activity.sponsorID==m_userID).all()
               for item in data:
                  ActivityFuction.response(item,self.retedata)
            except:
                self.retjson['code']=400
                self.retdata='no result found'
        elif type=='AskMyJoinActivity':#2.获得我参加的所有活动
            userID=self.get_argument('userID',default='unsolved')
            try:
               activityparticipate=self.db.query(ActivityParticipate).filter(ActivityParticipate.activity_participateID==userID).all()#返回activityparticipate元组
               for ID in activityparticipate:
                   item=self.db.query(Activity).filter(Activity.activityID==ID.activityID).one()
                   ActivityFuction.response(item, self.retedata)
            except MultipleResultsFound:
                self.retjson['code']=300
                self.retjson['content']=u'系统出错'
            except:
                self.retjson['code']=400
                retdata='no result found'
        elif type=='AskOneActivity':#3.获得某一个活动或更新活动
            activityID=self.get_argument('activityID',default='unsolved')
            try:
                data = self.db.query(Activity).filter(Activity.activityID == activityID).all()
                for item in data:
                   ActivityFuction.response(item, self.retedata)
            except:
                self.retjson['code'] = 400
                retdata = 'no result found'
        elif type=='AskParticipates': #4.获得活动的所有报名者
            m_activityID=self.get_argument('activityID',default='unsolved')
            try:
                registers=self.db.query(ActivityParticipate).filter(ActivityParticipate.activityID==m_activityID).all()
                for user in registers:
                    response=user.userID
                    try:
                       item=self.db.query(User).filter(User.userID==response).one()
                    except:
                        self.retjson['code']=300
                        self.retjson['content']=u'系统出错'
                    ActivityFuction.response(item,self.retdata)
            except:
                self.retjson['code'] = 400
                retdata = 'no result found'
        elif type=='AskOpenActivity': #5.获得所有未关闭的活动
            userID=self.get_arguments('userID',default='unsolved')
            try:
                data=self.db.query(Activity).filter(Activity.closed==False).all()
                for item in data:
                   ActivityFuction.response(item, self.retdata)
            except:
                self.retjson['code'] = 400
                retdata = 'no result found'

        self.retjson['content']=retdata
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))#返回中文



