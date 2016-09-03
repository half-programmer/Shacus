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
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: retjson
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
    def ap_Model_multiple(self, appointments, retdata):
        for item in appointments:
            m_response = dict(
                APid=item.APid,
                APtitle=item.APtitle,
                APsponsorid=item.APsponsorid,
                APtag=item.APtag,
                APtype=item.APtype,
                APlocation=item.APlocation,
                APstartT=item.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
                APendT=item.APendT.strftime('%Y-%m-%dT%H:%M:%S'),
                APjoinT=item.APjoinT.strftime('%Y-%m-%dT%H:%M:%S'),
                APcontent=item.APcontent,
                APfree=item.APfree,
                APprice=item.APprice,
                APclosed=item.APclosed,
                APcreateT=item.APcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
                APaddallowed=item.APaddallowed,
                APlikeN=item.APlikeN,
                APvalid=item.APvalid
            )
            retdata.append(m_response)

    @classmethod
    def ap_Model_simply_one(clas, appointment):
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: retjson
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
        except Exception,e:
            print e
        return ret_ap

    # @classmethod
    # def ApInforesponse(item, retdata):
    #         m_ApInforesponse = dict(
    #             AIid=item.AIid,
    #             AImid=item.AImid,
    #             AIpid=item.Aipid,
    #             AImscore=item.AImscore,
    #             AIpscore=item.AIpscore,
    #             AImcomment=item.AImcomment,
    #             AIpcomment=item.AIpcomment,
    #             AIappoid=item.AIappoid
    #         )
    #         retdata.append(m_ApInforesponse)
    #
    # @classmethod
    # def ApUserinfo(item, retdata):
    #         m_ApUserinfo = dict(
    #             Uid=item.Uid,  # 主键
    #             Upassword=item.Upassword,
    #             Utel=item.Utel,
    #             Ualais=item.Ualais,
    #             Uname=item.Uname,  # 真实姓名
    #             Ulocation=item.Ulocation,
    #             Umailbox=item.Umailbox,
    #
    #             Ubirthday=item.Ubirthday.strftime('%Y-%m-%dT%H:%M:%S'),
    #             Uscore=item.Uscore,
    #             UregistT=item.UregistT.strftime('%Y-%m-%dT%H:%M:%S'),
    #             Usex=item.Usex,
    #             Usign=item.Usign,
    #             Uauthkey=item.Uauthkey
    #         )
    #         retdata.append(m_ApUserinfo)
    #
    # @classmethod
    # def APinfochoose(item, item2, retdata):
    #         m_APinfochoose = dict(
    #             Uid=item.Uid,
    #             Usign=item.Usign,
    #             Ualais=item.Ualais,
    #             UIurl=item2.UIurl,
    #         )
    #         retdata.append(m_APinfochoose)




