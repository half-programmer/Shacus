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
    def ap_Model_simply_each(clas, appointment):
        ap_simply_info = dict(
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
            APclosed=appointment.APclosed,
            APcreateT=appointment.APcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
            APaddallowed=appointment.APaddallowed,
            APlikeN=appointment.APlikeN,
            APvalid=appointment.APvalid
        )


    @classmethod
    def ap_Model_multiple(self, appointment):
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
                APclosed=appointment.APclosed,
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
            return ret_ap
        except Exception,e:
            print e


    # @classmethod
    # def ApInforesponse(appointment, retdata):
    #         m_ApInforesponse = dict(
    #             AIid=appointment.AIid,
    #             AImid=appointment.AImid,
    #             AIpid=appointment.Aipid,
    #             AImscore=appointment.AImscore,
    #             AIpscore=appointment.AIpscore,
    #             AImcomment=appointment.AImcomment,
    #             AIpcomment=appointment.AIpcomment,
    #             AIappoid=appointment.AIappoid
    #         )
    #         retdata.append(m_ApInforesponse)
    #
    # @classmethod
    # def ApUserinfo(appointment, retdata):
    #         m_ApUserinfo = dict(
    #             Uid=appointment.Uid,  # 主键
    #             Upassword=appointment.Upassword,
    #             Utel=appointment.Utel,
    #             Ualais=appointment.Ualais,
    #             Uname=appointment.Uname,  # 真实姓名
    #             Ulocation=appointment.Ulocation,
    #             Umailbox=appointment.Umailbox,
    #
    #             Ubirthday=appointment.Ubirthday.strftime('%Y-%m-%dT%H:%M:%S'),
    #             Uscore=appointment.Uscore,
    #             UregistT=appointment.UregistT.strftime('%Y-%m-%dT%H:%M:%S'),
    #             Usex=appointment.Usex,
    #             Usign=appointment.Usign,
    #             Uauthkey=appointment.Uauthkey
    #         )
    #         retdata.append(m_ApUserinfo)
    #
    # @classmethod
    # def APinfochoose(appointment, appointment2, retdata):
    #         m_APinfochoose = dict(
    #             Uid=appointment.Uid,
    #             Usign=appointment.Usign,
    #             Ualais=appointment.Ualais,
    #             UIurl=appointment2.UIurl,
    #         )
    #         retdata.append(m_APinfochoose)




