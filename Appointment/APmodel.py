# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
'''
from BaseHandlerh import BaseHandler
from Database.tables import Appointment

class APmodelHandler:

    @classmethod
    def ap_Model_simply(clas,appointment):
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: retjson
        '''
        #todo:查找待变更为最新10个
        try:
            ap_simply_info = dict(
        APid=appointment.APid,
        APtitle=appointment.APtitle,
        APimgurl=r'http://image.baidu.com/search/detail?ct=503316480&z=&tn=baiduimagedetail&ipn=d&word=%E5%8D%95%E8%BA%AB%E7%8B%97&step_word=&ie=utf-8&in=&cl=2&lm=-1&st=-1&cs=2150404125,3211995021&os=1615331675,3944367252&simid=0,0&pn=8&rn=1&di=39492073940&ln=1989&fr=&fmq=1472862566666_R&ic=0&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&is=&istype=2&ist=&jit=&bdtype=0&adpicid=0&pi=0&gsm=0&objurl=http%3A%2F%2Fimg9.jiwu.com%2Fjiwu_news_pics%2F20151225%2F1450854576571_000.jpg&rpstart=0&rpnum=0&adpicid=0',
        APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
        APlikeN=appointment.APlikeN,
        APregistN=appointment.APregistN
        )
        except Exception,e:
            print e
        print '进入methodffffff'
        return ap_simply_info




def user_ap_simply(ap_info):
    ret_ap = {'apid': ap_info.APid, 'apsponsorid': ap_info.APsponsorid, 'aptitle': ap_info.APtitle,
              'aplocation': ap_info.APlocation, 'apvalid': ap_info.APvalid,'aptype':ap_info.APtype,
              }
    return ret_ap
