# coding=utf-8
from Database.tables import User, Activity,ActivityEntry
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
                if key == m_auth_key: # 认证成功
                    try:
                        activity = self.db.query(Activity).filter(Activity.ACtitle == m_title).one()
                        if activity:
                            self.retjson['code'] = '10312'
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
                            retjson_body['acID'] = ac_id[0];
                            self.retjson['code'] = '10313'
                            self.retjson['contents'] = retjson_body
                        except Exception,e:
                            print e
                            self.db.rollback()
                            self.retjson['code'] = '10319'
                            self.retjson['contents'] = r'服务器错误'
                else :
                    self.retjson['code'] = '10311'
                    self.retjson['contents'] = r'用户认证码错误'
            except Exception,e:
                print e
                self.retjson['code'] = '10310'
                self.retjson['contents'] = r'该用户不存在'

        elif ac_type ==  '10302': #开始传输数据
            print "进入10302，传输数据"
            ac_id = self.get_argument('acid')
            ac_title = self.get_argument('actitle')
            ac_auth_key = self.get_argument('authkey')
            ac_location = self.get_argument('location')
            ac_tag = self.get_argument('tags')
            ac_startT = self.get_argument('startT')
            ac_entT = self.get_argument('endT')
            ac_joinT = self.get_argument('joinT')
            ac_content = self.get_argument('content')
            ac_free = self.get_argument('free')
            ac_price = self.get_argument('price')
            ac_maxp = self.get_argument('maxp')
            ac_minp = self.get_argument('minp')
            try :
                user = self.db.query(User).filter(User.Uauthkey == ac_auth_key).one()
                ac_sponsorid = user.Uid
                try :
                    exist =self.db.query(Activity).filter(Activity.ACtitle == ac_title,Activity.ACid == ac_id
                                                          ,Activity.ACsponsorid == ac_sponsorid).one()
                    if exist: #验证用户授权成功
                        print '授权验证成功'
                        self.db.query(Activity).filter(Activity.ACid == ac_id).\
                            update({Activity.AClocation: ac_location,Activity.ACtag: ac_tag,
                                    Activity.ACstartT: ac_startT,Activity.ACendT:ac_entT,
                                    Activity.ACjoinT: ac_joinT,Activity.ACcontent: ac_content,
                                    Activity.ACfree: ac_free,Activity.ACprice: ac_price,
                                    Activity.ACmaxp: ac_maxp,Activity.ACminp: ac_minp},synchronize_session = False)
                        try :
                           self.db.commit()
                           self.retjson['code'] = '10323'
                           self.retjson['contents'] = '发布活动成功'
                        except Exception,e:
                            print e
                            self.rollback()
                            self.retjson['code'] = '10322'
                            self.retjson['contents'] = '服务器错误'
                except Exception,e:
                    print e
                    self.retjson['code'] = '10321'
                    self.retjson['contents'] = '该活动未授权'
            except Exception,e:
                print e
                self.retjson['code'] = '10320'
                self.retjson['contents'] = '用户授权码错误'

        elif ac_type == '10305': #报名活动
            ac_id = self.get_argument('acid')
            ac_registerid = self.get_argument('registerid')
            try :
                exist = self.db.query(ActivityEntry).filter(ActivityEntry.ACEacid == ac_id and
                                                            ActivityEntry.ACEregisterid == ac_registerid ).one()
                if exist.ACEregisttvilid :
                    self.retjson['contents'] = r'您已经报名该活动'
                    self.retjson['code'] = '10351'
                else: #用户曾经报名过该活动
                    self.db.query(ActivityEntry).\
                        filter(ActivityEntry.ACEacid == ac_id and ActivityEntry.ACEregisterid == ac_registerid ).\
                        update({ActivityEntry.ACEregisttvilid : 1},synchronize_session = False)
                    self.db.commit()
                    self.retjson['contents'] = r'您已报名成功'
                    self.retjson['code'] = '10352'
            except Exception,e: #用户从未报名过该活动
                print e
                new_activityEntry = ActivityEntry(
                    ACEacid = ac_id,
                    ACEregisterid = ac_registerid,
                    ACEregisttvilid = 1,
                    ACEscore = 0,
                    ACEcomment  = 0,
                )
                self.db.merge(new_activityEntry)
                try :
                    self.db.commit()
                    self.retjson['contents'] = r'您已报名成功'
                    self.retjson['code'] = '10352'
                except Exception,e:
                    print e
                    self.db.rollback()
                    self.retjson['contents'] = r'服务器出错'
                    self.retjson['code'] = '10359'

        elif ac_type == '10306': #用户取消报名活动
            ac_id = self.get_argument('acid')
            ac_registerid = self.get_argument('registerid')
            try:
                exist = self.db.query(ActivityEntry).filter(ActivityEntry.ACEacid == ac_id and
                                                            ActivityEntry.ACEregisterid == ac_registerid).one()
                if exist.ACEregisttvilid:
                    self.db.query(ActivityEntry). \
                        filter(ActivityEntry.ACEacid == ac_id and ActivityEntry.ACEregisterid == ac_registerid). \
                        update({ActivityEntry.ACEregisttvilid: 0})
                    self.db.commit()
                    self.retjson['contents'] = r'取消报名活动成功'
                    self.retjson['code'] = '10361'
                else:  # 用户曾经报名过该活动
                    self.retjson['contents'] = r'您未报名该活动'
                    self.retjson['code'] = '10352'
            except Exception, e:  # 用户从未报名过该用户
                print e
                self.retjson['contents'] = r'您未报名该活动'
                self.retjson['code'] = '10352'









        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

