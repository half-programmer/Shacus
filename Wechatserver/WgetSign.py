# -*- coding: utf-8 -*-

'''
@type:微信获取JSSDK签名
@author:兰威
@datatime : 2016.10.1
'''
import json

from BaseHandlerh import BaseHandler

from WJS import WJS
class WgetSign(BaseHandler):

    def post(self):
        ret = []

        type = self.get_argument('type')

        if type == '20001':
           wjs = WJS("lanwei")
           self.ret = wjs.sign()
        self.write(json.dump(self.ret,ensure_ascii=False, indent=2))





