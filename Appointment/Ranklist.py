# coding=utf-8
'''
@author:黄鑫晨
@create_time:2016-09-09
'''
import json
from Database.models import get_db
from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Database.tables import User, RankScore
from Userinfo import Usermodel
from Userinfo.Ufuncs import Ufuncs

global db
db = get_db()
class Ranklist(BaseHandler):
    '''
        用来与客户端通信的类
    '''
    retjson = {'code':'', "content": ''}
    def post(self):
        type = self.get_argument('type')
        u_auth_key = self.get_argument('authkey')
        uid = self.get_argument('uid')
        rank_list_handler = RanklistHandler()
        if Ufuncs.judge_user_valid(uid,u_auth_key):  # 用户验证成功
            if type == '10281':  # 请求摄影师排行
                self.retjson['content'] = rank_list_handler.get_model_list()
            elif type == '10282':  # 请求模特排行
                self.retjson['content'] = rank_list_handler.get_photoer_list()
        else:
            self.retjson['code'] = '10285'
            self.retjson['content'] = u'用户认证失败！'


class RanklistHandler(object):
    retjson = {'code': '', "content": ''}
    '''
        用来处理排行榜的计算的类
    '''
    def get_model_list(self):
        '''
        获取模特排行榜前十的RankScore模型
        Returns:获得前十模特的RankScore模型
        '''
        try:
            models = db.query(RankScore).filter(RankScore.RSMrank<=10).all()   # 排行榜前十的模特
            return models
        except Exception, e:
            print e, u'获取排行榜列表时出现异常'
            # self.retjson['code'] = '10286'
            # self.retjson['content'] = u'获取排行榜列表时出现异常'

    def get_photoer_list(self):
        '''
        获取摄影师排行榜前十的RankScore模型
        Returns:前十摄影师的RankScore模型
        '''
        try:
            photoers = db.query(RankScore).filter(RankScore.RSPrank<=10).all()  # 排行榜前十的摄影师
            return photoers
        except Exception, e:
            print e, u'获取排行榜列表时出现异常'
            # self.retjson['code'] = '10286'
            # self.retjson['content'] = u'获取排行榜列表时出现异常'

    def get_rank_photoers(self):
        '''
        Returns:获得前十名摄影师的用户模型
        '''
        photoers_user_models = self.get_rank_list_usermodel(self.get_photoer_list())  # 前十摄影师的用户模型
        return photoers_user_models

    def get_rank_models(self):
        '''
        Returns:得前十名模特的用户模型
        '''
        models_user_models = self.get_rank_list_usermodel(self.get_model_list())  # 前十模特的用户模型
        return  models_user_models


    def get_rank_list_usermodel(self, rs_models):
        '''
        Args:
            rs_pmodels: 前十摄影师的RankScore模型
        Returns:返回前十摄影师的用户模型
        '''
        user_models = []
        for rs_umodel in rs_models:
            rs_u_id = rs_umodel.RSuid  # 摄影师的用户id
            try:
                user = db.query(User).filter(User.Uid == rs_u_id).one()
                user_model = Usermodel.get_user_detail_from_user(user)
                user_models.append(user_model)

            except Exception, e:
                print e, u"未查找找到该用户"
                # self.retjson['code'] = '10285'
                # self.retjson['content'] = u"未查找找到该用户"
        return user_models

    def insert_new_rank(self,userid):
        '''
        用户初始化时，添加入新的排行榜
        Args:
            userid: 用户id
        Returns:
        '''
        try:
            rank_user = db.query(RankScore).filter(RankScore.RSuid == userid).one()
            if rank_user:
                print "该用户已初始化过！"
        except Exception, e:
            print e
            new_rs = RankScore(
                RSuid=userid,
                RSMscore=0,
                RSPscore=0,
                RSMrank=101,
                RSPrank=101
                )
            try:

                db.merge(new_rs)
                db.commit()
            except Exception, e:
                print e


