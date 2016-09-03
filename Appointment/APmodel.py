# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
'''
from BaseHandlerh import BaseHandler
from Database.tables import Appointment

class APmodelHandler:

    @classmethod
    def ap_Model_simply(self,appointment):
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: retjson
        '''
        #todo:查找待变更为最新10个

        ap_simply_info = dict(
        APid=appointment.APid,
        APtitle=appointment.APtitle,
        APimgurl='暂无',
        APstartT=appointment.APstartT.strftime('%Y-%m-%d %H:%M:%S'),
        APlikeN=appointment.APlikeN,
        APregistN=appointment.APregistN
        )
        return ap_simply_info





