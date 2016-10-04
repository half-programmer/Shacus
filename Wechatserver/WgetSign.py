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
            ip = self.request.remote_ip
            url = 'http://%s:80/WgetSign.html'%ip
            wjs = WJS(url)
            self.ret = wjs.sign()
        self.write(json.dumps(self.ret,ensure_ascii=False, indent=2))





