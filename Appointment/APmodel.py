# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
'''
from BaseHandlerh import BaseHandler
from Database.tables import Appointment

class APmodelHandler(object):

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
        APregistN=appointment.APregistN,
        Userimg = r"http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg"
        )
            return ap_simply_info
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




