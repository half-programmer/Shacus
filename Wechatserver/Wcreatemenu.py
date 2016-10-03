# -*- coding: utf-8 -*-
'''
微信创建菜单
'''
from wechat_sdk.exceptions import OfficialAPIError

from BaseHandlerh import BaseHandler
from Wconf import Wconf
from wechat_sdk import WechatBasic
class Wcreatmenu(BaseHandler):

    conf = Wconf.conf
    def createmenu(self):
        '''
        创建微信菜单
        Returns:

        '''
        wechat = WechatBasic(conf=self.conf)
        menu = {
            'button':[
                {
                    'type': 'click',
                    'name': '今日歌曲',
                    'key': 'V1001_TODAY_MUSIC'
                },
                {
                    'type': 'click',
                    'name': '歌手简介',
                    'key': 'V1001_TODAY_SINGER'
                },
                {
                    'name': '菜单',
                    'sub_button': [
                        {
                            'type': 'view',
                            'name': '搜索',
                            'url': 'http://www.soso.com/'
                        },
                        {
                            'type': 'view',
                            'name': '视频',
                            'url': 'http://v.qq.com/'
                        },
                        {
                            'type': 'click',
                            'name': '赞一下我们',
                            'key': 'V1001_GOOD'
                        }
                    ]
                }
            ]
        }
        try:
            wechat.create_menu(menu)
        except OfficialAPIError,e:
            print e