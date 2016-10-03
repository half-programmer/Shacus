# -*- coding: utf-8 -*-

'''
@type:微信基本配置
@author:兰威
@datatime : 2016.10.1
'''

from wechat_sdk import WechatConf
from BaseHandlerh import BaseHandler
from Database.tables import WeAcToken
from Database.models import get_db
class Wconf(BaseHandler):

    def get_access_token_function(self):
        '''
        获取access_token
        :return: 注意返回值为一个 Tuple，第一个元素为 access_token 的值，第二个元素为 access_token_expires_at 的值
        '''
        db = get_db()
        access_token = db.query(WeAcToken.WACtoken).all()
        expires = db.query(WeAcToken.WACexpire).all()
        token = (access_token[0],expires[0])
        return token

    def set_access_token_function(access_token, access_token_expires_at):
        db = get_db()
        weactoken = db.query(WeAcToken).all()
        if weactoken == []:
            actoken = WeAcToken(
                WACexpire=access_token_expires_at,
                WACtoken=access_token,
            )
            db.merge(actoken)
        else:
            weactoken[0].WACexpire = access_token_expires_at
            weactoken[0].WACtoken = access_token
        try:
            db.commit()
        except Exception, e:
            print e
            db.roolback()

    conf = WechatConf(
        token='xtIRzP0tcQuGqcgWiu',
        appid='wx679493e73b1bd83b',
        appsecret='f1dad656a7269b068834b5007991b46b',
        encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
        #encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
        access_token_getfunc=get_access_token_function,
        access_token_setfunc=set_access_token_function,

    )


