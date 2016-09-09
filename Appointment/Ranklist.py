# coding=utf-8
import json
from Database.models import get_db
from sqlalchemy import desc

from  BaseHandlerh import BaseHandler
from Database.tables import User, AppointEntry, Appointment, RankScore
from Userinfo import Usermodel
from Userinfo.Ufuncs import Ufuncs

class Ranklist(BaseHandler):
    '''
        用来与客户端通信的类
    '''
    retjson = {'code':'', "content": ''}
    def post(self):
        type = self.get_argument('type')
        u_auth_key = self.get_argument('authkey')
        uid = self.get_argument('uid')
        if Ufuncs.judge_user_valid(uid,u_auth_key):  # 用户验证成功
            if type == '10281':  # 请求摄影师排行

            elif type == '10282':  # 请求模特排行

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
        获取排行榜前十
        Returns:获得前十模特的RankScore模型
        '''
        try:
            models = get_db().query(RankScore).filter(RankScore.RSMrank<=10).all()   # 排行榜前十的模特
            return models
        except Exception, e:
            print e
            self.retjson['code'] = '10286'
            self.retjson['content'] = u'获取排行榜列表时出现异常'

    def get_photoer_list(self):
        '''
        获取摄影师排行榜前十
        Returns:获得前十摄影师的RankScore模型
        '''
        try:
            photoers = get_db().query(RankScore).filter(RankScore.RSPrank<=10).all()  # 排行榜前十的摄影师
            return photoers
        except Exception, e:
            print e
            self.retjson['code'] = '10286'
            self.retjson['content'] = u'获取排行榜列表时出现异常'

    def get_photort_list_usermodel(self,rs_pmodels):
        '''
        Args:
            rs_pmodels: 获得前十摄影师的RankScore模型

        Returns:返回前十摄影师的用户模型
        '''
        for rs_pmodel in rs_pmodels:
            rs_p_id = rs_pmodel.RSuid  # 摄影师的用户id
            try:
                user = get_db().query(User).filter(User.Uid == rs_p_id).one()
                user_model = Usermodel.get_user_detail_from_user(user)

            except Exception, e:
                self.retjson['code'] = '10285'
                self.retjson['content'] = u"未查找找到该用户"


