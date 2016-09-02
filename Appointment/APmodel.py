# coding=utf-8
'''返回不同格式的约拍模型
@author：黄鑫晨
@
'''
from BaseHandlerh import BaseHandler

def get_db():
    '''
    获得数据库
    :return: db
    '''
    basehandler = BaseHandler()
    db = basehandler.db
    return db

def ap_model_simply():
    '''得到简单约拍模型，用于登录首页
    :return:  retjson
    '''
    db = get_db()
    db.query
def user_ap_simply(ap_info):
    ret_ap = {'apid': ap_info.APid, 'apsponsorid': ap_info.APsponsorid, 'aptitle': ap_info.APtitle,
              'aplocation': ap_info.APlocation, 'apvalid': ap_info.APvalid,'aptype':ap_info.APtype,
              }
    return ret_ap