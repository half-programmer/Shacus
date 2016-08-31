# -*- coding: utf-8 -*-

"""
 Hxc于2016.6.26
TODO: 报名
"""
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,ForeignKey,DateTime,Boolean
from sqlalchemy.types import CHAR, Integer, VARCHAR,Boolean,Float
from sqlalchemy.sql.functions import func
from models import Base
import sys
reload(sys)

# from models import engine

# 每个类对应一个表
class User(Base): # 用户表
    __tablename__ = 'User'

    Uid = Column(Integer, nullable=False, primary_key=True)  # 主键
    Upassword = Column(VARCHAR(16), nullable=False)
    Utel = Column(CHAR(11),nullable=False,unique=True,)
    Ualais = Column(VARCHAR(24),nullable=False,unique=True) # 昵称
    Uname = Column(VARCHAR(24),nullable=True) # 真实姓名
    Ulocation = Column(VARCHAR(128))
    Umailbox = Column(VARCHAR(32))#unique=True) # unique表示唯一性
    Ubirthday = Column(DateTime)
    Uscore = Column(Integer, default=0)
    UregistT = Column(DateTime(timezone=True), default=func.now())
    Usex = Column(Boolean,nullable=False)
    Usign = Column(VARCHAR(256))
    Uauthkey = Column(VARCHAR(32))

class Verification(Base): # 短信验证码及生成用户auth_key时间
    __tablename__ = 'Verification'

    Vphone = Column(CHAR(11),primary_key=True) #
    Vcode = Column(CHAR(6),nullable=False)
    VT = Column(DateTime(timezone=True), default=func.now()) # 待测试是插入数据的时间还是最后一次更新该表的时间 （测试结果为第一次插入时间）

class Activity(Base):#活动表
    __tablename__ = 'Activity'

    ACid = Column(Integer,nullable=False, primary_key=True)
    ACsponsorid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))  #活动发起者
    AClocation = Column(VARCHAR(128), nullable=False)
    ACtitle = Column(VARCHAR(24), nullable=False) # 活动的名称？确认长度
    ACtag = Column(VARCHAR(12)) # 活动的标签？确认类型
    ACstartT = Column(DateTime, nullable=False)
    ACendT = Column(DateTime, nullable=False)
    ACjoinT = Column(DateTime) # 活动报名截止时间
    ACcontent = Column(VARCHAR(128), nullable=False) # 活动介绍
    ACfree = Column(Boolean)
    ACprice = Column(Float)
    ACclosed = Column(Boolean,default=1, nullable=False) # 活动是否已经结束
    ACcreateT = Column(DateTime(timezone=True), default=func.now())
    ACcommentnumber = Column(Integer,default=0, nullable=False)
    ACmaxp = Column(Integer)
    ACminp = Column(Integer)
    ACscore = Column(Integer,default=0)
    AClikenumber = Column(Integer,default=0)
    ACvalid = Column(Boolean,default=1) # 活动是否已经删除


class ActivityEntry(Base):  #活动报名表
    __tablename__ = 'Activityaentry'

    ACEid=Column(Integer,primary_key=True)
    ACEacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))#活动ID
    ACEregisterid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))#报名人ID
    ACEregisttvilid = Column(Boolean,default=1)
    ACEscore = Column(Integer)
    ACEcomment = Column(VARCHAR(128))
    ACEregisterT = Column(DateTime(timezone=True), default=func.now())

class ActivityLike(Base):
    __tablename__ = 'ActivityLike'

    ACLid=Column(Integer,primary_key=True)
    ACLacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))
    ACLuid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))
    ACLvalid = Column(Boolean)
    ACLT = Column(DateTime)

class CheckIn(Base):
    __tablename__ = 'CheckIn'

    # 复合主键
    CLuid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),primary_key=True)
    CLcheckday = Column(DateTime(timezone=True), default=func.now())


class UserLike(Base):
    __tablename__ = 'UserLike'

    ULid=Column(Integer,primary_key=True)
    ULlikeid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))
    ULlikedid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))
    ULvalid = Column(Boolean,default=1)
    ULlikeT = Column(DateTime(timezone=True), default=func.now())

class Image(Base):
    __tablename__ = 'Image'

    IMid = Column(Integer,primary_key=True,nullable=False)
    IMvalid = Column(Boolean,default=1)
    IMT = Column(DateTime(timezone=True), default=func.now())
    IMname = Column(VARCHAR(128), nullable=False)

class ActivityImage(Base):
    __tablename__ = "ActivityImage"

    ACIacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))
    ACIimid = Column(Integer,ForeignKey('Image.IMid',onupdate='CASCADE'),primary_key=True)
    ACIurl = Column(VARCHAR(128))#数据长度

class AppointmentImage(Base):
    __tablename__ = 'AppointImage'

    APIapid = Column(Integer,ForeignKey("Appointment.APid",onupdate="CASCADE"))
    APIimid = Column(Integer,ForeignKey("Image.IMid",onupdate="CASCADE"),primary_key=True)
    APIurl = Column(VARCHAR(128))

class UserImage(Base):
    __tablename__ = 'UserImage'

    UIuid = Column(Integer,ForeignKey("User.Uid",onupdate="CASCADE"))
    UIimid = Column(Integer,ForeignKey("Image.IMid",onupdate="CASCADE"),primary_key=True)
    UIurl = Column(VARCHAR(128))

class Appointment(Base):  #摄影师-模特约拍
    __tablename__ = 'Appointment'

    APid = Column(Integer, primary_key=True,nullable=False)
    APsponsorid = Column(Integer, ForeignKey('User.Uid', ondelete='CASCADE'), nullable=False)  # 发起者
    APtitle=Column(VARCHAR(24),nullable=False)
    APlocation = Column(VARCHAR(128), nullable=False)
    APtag=Column(VARCHAR(12)) # 约拍标签？确认长度
    APstartT = Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APendT = Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APjoinT=Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APcontent=Column(VARCHAR(128), nullable=False, default='')
    APfree = Column(Boolean)
    APprice = Column(Float)
    APclosed = Column(Boolean)
    APcreateT = Column(DateTime(timezone=True), default=func.now())
    APtype = Column(Boolean,nullable=False,default=0) # 约拍类型，模特约摄影师(1)或摄影师约模特(0)
    APaddallowed = Column(Boolean,default=0)
    APlikeN = Column(Integer, default=0, nullable=False)
    APvalid = Column(Boolean, default=1, nullable=False)


class AppointmentInfo(Base):
    __tablename__ = "Appointmentinfo"

    AIid = Column(Integer,primary_key=True)
    AImid = Column(Integer,ForeignKey('User.Uid', ondelete='CASCADE'))
    AIpid = Column(Integer,ForeignKey('User.Uid', ondelete='CASCADE'))
    AImscore = Column(Integer,default=0)
    AIpscore = Column(Integer,default=0)
    AImcomment = Column(VARCHAR(128))
    AIpcomment = Column(VARCHAR(128))
    AIappoid = Column(Integer,ForeignKey('Appointment.APid',onupdate='CASCADE'))#与AIid相同，是否重复？

class AppointEntry(Base):
    __tablename__ = "AppointEntry"

    AEid = Column(Integer,primary_key=True)
    AEregisterID = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))
    AEvalid = Column(Boolean)
    AEchoosed = Column(Boolean)
    AEregistT = Column(DateTime(timezone=True), default=func.now())

class AppointLike(Base):
    __tablename__ = 'AppointLike'

    ALid=Column(Integer,primary_key=True)
    ALapid = Column(Integer,ForeignKey('Appointment.APid',onupdate='CASCADE'))
    ALuid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))
    ALvalid = Column(Boolean)
    ALT = Column(DateTime(timezone=True), default=func.now())





