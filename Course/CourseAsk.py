# coding=utf-8
'''返回不同格式的教程模型
@author：兰威
'''
import json

from BaseHandlerh import BaseHandler
from Course import Coursemodel
from Database.tables import Course, CourseTagEntry, CourseTag, CourseLike, Usercourse
from Userinfo import Ufuncs


class CourseAsk(BaseHandler):
    retjson ={'code':'','contents':''}
    def post(self):
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, u_authkey):
            type = self.get_argument('type')

            if type =='11002':    #请求教程的详细信息
                c_id = self.get_argument('cid')
                tags = []
                ret_content ={}
                try:
                    exist = self.db.query(Usercourse).filter(Usercourse.UCcid == c_id,Usercourse.UCuid == u_id).one() #判断是否曾经看过此教程
                    if exist.UCseen == 0 :
                        exist.UCseen =1
                        self.db.commit()
                except Exception,e:
                    entry = Usercourse(
                        UCuid = u_id,
                        UCcid = c_id,
                        UCseen =1,
                        UCfav =0
                    )
                    self.db.merge(entry)
                    self.db.commit()


                course = self.db.query(Course).filter(Course.Cid == c_id).one()
                entrys = self.db.query(CourseTagEntry).filter(CourseTagEntry.CTEcid == c_id,
                                                            CourseTagEntry.CTEvalid == 1).all()         #查询教程的标签
                for entry in entrys:
                    tag_info = self.db.query(CourseTag).filter(CourseTag.CTid == entry.CTEtid).one()
                    tags.append(tag_info.CTname)
                ret_content ['course']= Coursemodel.Coursemodel.Course_Model_Complete(course,tags)
                course.CwatchN+=1
                self.db.commit()
                try:
                    self.db.query(CourseLike).filter(CourseLike.CLcid ==c_id,
                                                         CourseLike.CLuid == u_id,
                                                         CourseLike.CLvalid == 1).one()
                    ret_content['isliked'] = 1
                except Exception,e:
                    ret_content['isliked'] = 0

                self.retjson['code'] = '11021'
                self.retjson['contents'] = ret_content

            if type == '11005':  # 返回我看过的所有教程
                ret_content={}
                ret_course =[]
                u_courses = self.db.query(Usercourse).filter(Usercourse.UCuid == u_id,Usercourse.UCseen == 1).all()
                for u_course in u_courses:
                    u_cid = u_course.UCcid
                    course = self.db.query(Course).filter(Course.Cid == u_cid).one()
                    ret_course.append(Coursemodel.Coursemodel.Course_Model_Simply_Homepage(course))
                ret_content['course'] =ret_course
                #self.db.query(CourseLike).filter(CourseLike.)



        else :
            self.retjson['code']  ='11000'
            self.retjson['contents'] = '用户授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))