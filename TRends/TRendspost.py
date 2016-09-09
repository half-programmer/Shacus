# -*- coding: utf-8 -*-

import json
import TRfunction
from BaseHandlerh import BaseHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import Trend, TrendImage, Image


class TRendspost(BaseHandler):
    retjson = {'code':'200','contents':'null'}
    def post(self):
       retdata = []
       type = self.get_argument('type',default='unsolved')
       if type == '12001':
           u_id = self.get_argument('uid',default='null')
           u_auth_key = self.get_argument('authkey',default='null')
           #a_auth = AuthKeyHandler
           #image_urls = []
           ufuncs = Ufuncs() #判断用户权限
           if ufuncs.judge_user_valid(u_id , u_auth_key):#认证成功
               data=self.db.query(Trend).all()
               for i in range(len(data)):
                   print '哈哈哈哈'
                   try:
                       url=self.db.query(TrendImage).filter(TrendImage.TItid==data[i].Tid).one()
                       #self.db.query(Image).filter(Image.IMid== url.TIimid)
                       TRfunction.TRresponse(data[i],url.TIimgurl,retdata)
                   except Exception,e:
                       print e
               self.retjson['code']='12013'
               self.retjson['contents'] =retdata
           else:
               self.retjson['code']='12012'
               self.retjson['contents']='用户认证失败'


       self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

