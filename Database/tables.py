# -*- coding: utf-8 -*-

"""
 Hxc于2016.6.26
TODO: 报名
"""
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,ForeignKey,DateTime,Boolean
from sqlalchemy.types import CHAR, Integer, VARCHAR
import sys
reload(sys)
from models import Base
# from models import engine

# 每个类对应一个表
class User(Base): # 用户表
    __tablename__ = 'User'

    userID = Column(Integer, nullable=False, primary_key=True)  # 主键
    password = Column(VARCHAR(64), nullable=False)  # 密码
    phone = Column(VARCHAR(11),nullable=False)  # 手机
    nick_name = Column(VARCHAR(64), nullable=False)  # 昵称
    real_name = Column(VARCHAR(64))
    level = Column(Integer, default=1)  # 等级
    location = Column(VARCHAR(128))  # 住址
    birthday = Column(DateTime)  # 生日

    regist_time = Column(DateTime)  # 注册时间


class Activity(Base):
    __tablename__ = 'Activity'

    activityID = Column(Integer, nullable=False, primary_key=True)
    sponsorID = Column(Integer, ForeignKey('User.userID',  onupdate='CASCADE'),nullable=False )  # 发起人,外健
    sponsor_time = Column(DateTime)  # 发起时间
    activity_name = Column(VARCHAR(128), nullable=False)
    activity_introduction = Column(VARCHAR(256), nullable=False)  #活动介绍
    type = Column(VARCHAR(64))  # 约拍类型
    location = Column(VARCHAR(128), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    min_people = Column(Integer, nullable=False)
    max_people = Column(Integer, nullable=False)
    closed = Column(Integer, nullable=False)
    imageurl = Column(VARCHAR(128))


class ActivityParticipate(Base):  #活动参与者的集合
    __tablename__ = 'ActivityParticipate'

    activity_participateID = Column(Integer, nullable=False, primary_key=True)
    activityID = Column(Integer, ForeignKey('Activity.activityID',  onupdate='CASCADE'))


class Style(Base):  # 约拍风格
    __tablename__ = 'Style'

    styleID = Column(Integer, primary_key=True, nullable=False)
    style_name = Column(VARCHAR(64), nullable=False)
    referenced_count = Column(VARCHAR(256))


class Estimation(Base):  # 摄影师-模特约拍评价表
    __tablename__ = 'Estimation'

    esti_userID = Column(Integer,  ForeignKey('User.userID', onupdate='CASCADE'), nullable=False, primary_key=True)
    beestied_userID = Column(Integer, nullable=False)  # 被评价的
    score = Column(Integer, nullable=False)
    appointmentID = Column(Integer, ForeignKey('Appointment.appointmentID', onupdate='CASCADE'), nullable=False)
    esti_time = Column(DateTime)  # 评价时间

class Appointment(Base):  #摄影师-模特约拍
    __tablename__ = 'Appointment'

    appointmentID = Column(Integer, primary_key=True)
    sponsorID = Column(Integer, ForeignKey('User.userID', ondelete='CASCADE'), nullable=False)  # 发起者
    location = Column(VARCHAR(128), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    appointment_name = Column(VARCHAR(128))
    appointment_introduction = Column(VARCHAR(128))
    self_introduction = Column(VARCHAR(128))
    styleID = Column(Integer, ForeignKey('Style.styleID', ondelete='CASCADE'))
    closed = Column(Boolean)
    create_time = Column(DateTime)  # 创建时间
    imageurl = Column(VARCHAR(128))

class AppointmenmtEntry(Base):  # 每次约拍参与者
    __tablename__ = 'AppointmentEntry'

    appointmentID = Column(Integer, ForeignKey('Appointment.appointmentID',  onupdate='CASCADE', ondelete='CASCADE'), nullable=False, primary_key=True)
    photographerID = Column(Integer, ForeignKey('User.userID',  onupdate='CASCADE', ondelete='CASCADE'))
    modelID = Column(Integer, ForeignKey('User.userID',  onupdate='CASCADE', ondelete='CASCADE'))


class AppointmentRegister(Base):  # 记录每个约拍的报名人
    __tablename__ = "AppointmentRegister"

    appointmentID = Column(Integer, ForeignKey('Appointment.appointmentID',  onupdate='CASCADE', ondelete='CASCADE'), primary_key=True) # todo 改主键待定义
    registerID = Column(Integer, ForeignKey('User.userID',  onupdate='CASCADE', ondelete='CASCADE'))  #
    regist_time = Column(DateTime)  # 报名时间

class Verification(Base):#记录每个用户的验证码和手机
    __tablename__="Verification"

    phone=Column(VARCHAR(11),primary_key=True)#手机号码，且为主键
    verificationcode=Column(VARCHAR(6))


# Base.metadata.create_all(engine)



