# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
'''
from BaseHandlerh import BaseHandler
from Database.tables import Appointment

class APmodelHandler(object):

    @classmethod
    def ap_Model_simply(clas, appointments, retdata):
        '''简单约拍模型，用于登录首页
        :param appointment: 传入多个appointment对象
        :return: 返回多个简单约拍模型
        '''
        #todo:查找待变更为最新10个
        try:
            for appointment in appointments:
                ap_simply_info = dict(
                     APid=appointment.APid,
                     APtitle=appointment.APtitle,
                     APimgurl=r"http://img9.jiwu.com/jiwu_news_pics/20151225/1450854576571_000.jpg",
                     APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
                     APlikeN=appointment.APlikeN,
                     APregistN=appointment.APregistN,
                     Userimg=r"http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg"
                      )
                retdata.append(ap_simply_info)
            return retdata
        except Exception, e:
            print e

    @classmethod
    def ap_Model_simply_one(clas, appointment):
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: 返回单个约拍简单模型
        '''
        # todo:查找待变更为最新10个
        try:
            ret_ap = dict(
                APid=appointment.APid,
                APtitle=appointment.APtitle,
                APimgurl=r"http://img9.jiwu.com/jiwu_news_pics/20151225/1450854576571_000.jpg",
                        APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
                        APlikeN=appointment.APlikeN,
                        APregistN=appointment.APregistN,
                        Userimg=r"http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg"
                )
            return ret_ap
        except Exception, e:
            print e

    @classmethod
    def ap_Model_multiple(clas, appointment):
            m_response = dict(
                APid=appointment.APid,
                APtitle=appointment.APtitle,
                APsponsorid=appointment.APsponsorid,
                APtag=appointment.APtag,
                APtype=appointment.APtype,
                APlocation=appointment.APlocation,
                APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
                APendT=appointment.APendT.strftime('%Y-%m-%dT%H:%M:%S'),
                APjoinT=appointment.APjoinT.strftime('%Y-%m-%dT%H:%M:%S'),
                APcontent=appointment.APcontent,
                APfree=appointment.APfree,
                APprice=appointment.APprice,
                APcreateT=appointment.APcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
                APaddallowed=appointment.APaddallowed,
                APlikeN=appointment.APlikeN,
                APvalid=appointment.APvalid,
                APregistN=appointment.APregistN,
                Userimg="http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg",
                APimgurl=[r"http://img9.jiwu.com/jiwu_news_pics/20151225/1450854576571_000.jpg", "http://p1.gexing.com/G1/M00/57/8B/rBACFFPcOFOiwBGVAACdMkF5UnM383.jpg","http://p1.gexing.com/G1/M00/57/8B/rBACFFPcOFOiwBGVAACdMkF5UnM383.jpg"],
                APstatus=appointment.APstatus
            )

            return m_response

    @classmethod
    def ApInforesponse(appointment, retdata):
        '''
        Returns:返回选择约拍的人关于约拍的详细信息

        '''
        m_ApInforesponse = dict(
                AIid=appointment.AIid,
                AImid=appointment.AImid,
                AIpid=appointment.Aipid,
                AImscore=appointment.AImscore,
                AIpscore=appointment.AIpscore,
                AImcomment=appointment.AImcomment,
                AIpcomment=appointment.AIpcomment,
                AIappoid=appointment.AIappoid
        )
        retdata.append(m_ApInforesponse)




