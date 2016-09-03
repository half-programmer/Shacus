# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
'''
from BaseHandlerh import BaseHandler
from Database.tables import Appointment

class APmodelHandler:

    @classmethod
    def ap_Model_simply(appointment):
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: retjson
        '''
        #todo:查找待变更为最新10个

        ap_simply_info = dict(
        APid=appointment.APid,
        APtitle=appointment.APtitle,
        APimgurl='暂无',
        APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
        APlikeN=appointment.APlikeN,
        APregistN=appointment.APregistN
        )
        return ap_simply_info




def user_ap_simply(ap_info):
    ret_ap = {'apid': ap_info.APid, 'apsponsorid': ap_info.APsponsorid, 'aptitle': ap_info.APtitle,
              'aplocation': ap_info.APlocation, 'apvalid': ap_info.APvalid,'aptype':ap_info.APtype,
              }
    return ret_ap
