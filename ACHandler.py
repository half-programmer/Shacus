# -*- coding :utf8 -*-
from Database.tables import User, Activity
from FileHandler.Upload import AuthKeyHandler
__author__='兰威'
'''
2016.08.30
'''
import json

from BaseHandlerh import BaseHandler

class ActivityCreate(BaseHandler):   #创建活动
    retjson={'code':'10300','contents':'None'}
    def post(self):
        ac_type = self.get_argument('type')
        if ac_type == '10301':  #活动第一个请求，用于同意发布活动，同时返回图片上传token
            print "进入创建活动"
            m_user_phone = self.get_argument('username')
            m_auth_key = self.get_argument('auth_key')
            m_title = self.get_argument('title')
            m_image = self.get_argument('images')
            try:
                sponsor = self.db.query(User).filter(User.Utel==m_user_phone).one()
                key = sponsor.Uauthkey
                m_sponsorid = sponsor.Uid
                if key == m_auth_key:
                    try:
                        activity = self.db.query(Activity).filter(Activity.ACtitle == m_title).one()
                        if activity:
                            self.retjson['code'] = '10303'
                            self.retjson['contents'] = r'该活动名称已经存在'
                    except Exception,e:
                        print e
                        retjson_body = {'image_token':'','acID':''}
                        image_token_handler = AuthKeyHandler()
                        m_image_json = json.loads(m_image)
                        retjson_body['image_token'] =  image_token_handler.generateToken(m_image_json)

                        my_activity = Activity(
                            ACsponsorid = m_sponsorid,
                            AClocation = '',
                            ACtitle = m_title,
                            ACtag = '',
                            ACstartT = '0000-00-00 00:00:00',
                            ACendT = '0000-00-00 00:00:00',
                            ACjoinT = '0000-00-00 00:00:00',
                            ACcontent = '',
                            ACfree = 0,
                            ACprice = 0,
                            ACclosed = 0,
                            ACcommentnumber = 0,
                            ACmaxp = 0,
                            ACminp = 0,
                            AClikenumber = 0,
                            ACvalid = 1

                        )
                        self.db.merge(my_activity)
                        try :
                            self.db.commit()
                            ac_id = self.db.query(Activity.ACid).filter(
                                Activity.ACtitle == m_title and Activity.ACsponsorid == m_sponsorid
                            ).one()
                            retjson_body['acID'] = ac_id;
                            self.retjson['code'] = '10304'
                            self.retjson['contents'] = retjson_body
                        except Exception,e:
                            print e
                            self.db.rollback()
                            self.retjson['code'] = '10309'
                            self.retjson['contents'] = r'服务器错误'


                else :
                    self.retjson['code'] = '10302'
                    self.retjson['contents'] = r'用户认证码错误'


            except Exception,e:
                print e
                self.retjson['code'] = '10301'
                self.retjson['contents'] = r'该用户不存在'



