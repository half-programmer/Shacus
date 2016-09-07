# coding=utf-8

'''
@author：兰威
@time :2016.9.6
'''
import json

from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Coursemodel import Coursemodel
from Documents.tables import Course, CourseTag
from Userinfo import Ufuncs

class Chomepage(BaseHandler):# 教程首页
    retjson ={ "code": '','contents':''}

    def post(self):
        ret_contents = {}
        ret_course = []
        ret_tag = []
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id,u_authkey):
            type = self.get_argument('type')
            if type == '11001':  #查看教程首页
                try:
                    courses = self.db.query(Course).filter(Course.Cvalid ==1).order_by(desc(Course.Cscore)).limit(3).all() #通过score查出前三推荐给用户
                except Exception,e:
                    print e
                for course in courses:
                    ret_course.append(Coursemodel.Course_Model_Simply_Homepage(course))
                tags = self.db.query(CourseTag).all()
                for tag in tags:
                    ret_tag.append(Coursemodel.CourseTag_Model(tag))
                ret_contents['tag'] = ret_tag
                ret_contents['course'] = ret_course
                self.retjson['contents'] = ret_contents
                self.retjson['code'] = '11010'
        else :
            self.retjson['contents'] = '用户授权码不正确'
            self.retjson['code'] = '11000'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
