# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@attention: Model为模型，model为模特
'''
from Database.models import get_db
from Database.tables import AppointLike, AppointmentImage
from Userinfo.Ufuncs import Ufuncs


class APmodelHandler(object):

    @classmethod
    def ap_Model_simply(clas, appointments, retdata, userid):
        '''简单约拍模型，用于登录首页
        :param appointment: 传入多个appointment对象
        :return: 返回多个简单约拍模型
        '''
        #todo:查找待变更为最新10个
        liked = 0
        try:
            for appointment in appointments:
                retdata.append(APmodelHandler.ap_Model_simply_one(appointment,userid))
            return retdata
        except Exception, e:
            print e
    @classmethod
    def ap_get_imgs_from_apid(clas, appointmentid):
        '''
        得到某约拍的图片
        Args:
            appointmentid: 约拍Id

        Returns:图片名数组

        '''
        img_urls = []
        imgs = get_db().query(AppointmentImage).filter(AppointmentImage.APIapid == appointmentid).all()  # 返回所有图片项
        for img in imgs:
            img_url = imgs.APIurl
            

    @classmethod
    def ap_Model_simply_one(clas, appointment, userid):
        '''得到简单约拍模型，用于登录首页
        :param appointment: 传入一个appointment对象
        :return: 返回单个约拍简单模型
        '''
        # todo:查找待变更为最新10个
        APmodelHandler.ap_get_imgs_from_apid(appointment.APid)
        liked = 0
        try:
            likedentry = get_db().query(AppointLike).filter(AppointLike.ALuid == userid,
                                                             AppointLike.ALapid == appointment.APid,
                                                             AppointLike.ALvalid == 1).one()  # 寻找是否点过赞
            if likedentry:
                liked = 1
                print "点过赞", liked
        except Exception, e:
              print e
              liked = 0

        #todo:userliked不对
        ret_ap = dict(
            APid=appointment.APid,
                APtitle=appointment.APtitle,
                APimgurl=r"http://img9.jiwu.com/jiwu_news_pics/20151225/1450854576571_000.jpg",
                APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
                APlikeN=appointment.APlikeN,
                APregistN=appointment.APregistN,
                Userimg=r"http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg",
                Userliked=liked
                )
        return ret_ap


    @classmethod
    def ap_Model_multiple(clas, appointment, userid):
        ap_regist_users = []

        liked = 0
        try:
            likedentry = get_db().query(AppointLike).filter(AppointLike.ALuid == userid,
                                                            AppointLike.ALapid == appointment.APid,
                                                            AppointLike.ALvalid == 1).one()  # 寻找是否点过赞
            if likedentry:
                liked = 1
                print "点过赞", liked
        except Exception, e:
            print e
            liked = 0
        try:
            ap_regist_users = Ufuncs.get_userlist_from_ap(appointment.APid)
            m_response = dict(
                APid=appointment.APid,
                APtitle=appointment.APtitle,
                APsponsorid=appointment.APsponsorid,
                APtag=appointment.APtag,
                APtype=int(appointment.APtype),
                APlocation=appointment.APlocation,
                APstartT=appointment.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
                APendT=appointment.APendT.strftime('%Y-%m-%dT%H:%M:%S'),
                APjoinT=appointment.APjoinT.strftime('%Y-%m-%dT%H:%M:%S'),
                APcontent=appointment.APcontent,
                APfree=int(appointment.APfree),
                APprice=appointment.APprice,
                APcreateT=appointment.APcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
                APaddallowed=int(appointment.APaddallowed),
                APlikeN=appointment.APlikeN,
                APvalid=int(appointment.APvalid),
                APregistN=appointment.APregistN,
                APregisters=ap_regist_users,  # 返回所有报名人用户模型
                APimgurl=[r"http://img9.jiwu.com/jiwu_news_pics/20151225/1450854576571_000.jpg", "http://p1.gexing.com/G1/M00/57/8B/rBACFFPcOFOiwBGVAACdMkF5UnM383.jpg","http://p1.gexing.com/G1/M00/57/8B/rBACFFPcOFOiwBGVAACdMkF5UnM383.jpg"],
                APstatus=appointment.APstatus,
                Userliked=liked
            )
            return m_response
        except Exception, e:
            print e




    @classmethod
    def ApInforesponse(appointment, retdata):
        '''
        Returns:返回选择约拍的人关于约拍的详细信息
        #todo:查找待变更为最新10个
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




