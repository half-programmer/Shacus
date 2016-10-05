# -*- coding: utf-8 -*-

'''
@type:微信获取JSSDK签名
@author:兰威
@datatime : 2016.10.1
'''
import json

from BaseHandlerh import BaseHandler

from WJS import WJS
from Wconf import Wconf
class WgetSign(BaseHandler):

    def get(self):
        ret = []
        conf = Wconf.conf

        type = self.get_argument('type')
        appsecret = self.get_argument("appsecret")
        if appsecret == conf.appsecret and type == 'getSignature':
            ip = self.request.remote_ip
            url = 'http://%s:80/WgetSign.html'%ip
            wjs = WJS(url)
            ret = wjs.sign()
        self.write(json.dumps(ret,ensure_ascii=False, indent=2))





