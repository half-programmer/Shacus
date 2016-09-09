# coding=utf-8
'''
@author :兰威
@type ： 用于获得用户聊天时的token
'''
import os

import requests

from rongcloud import RongCloud





import os
from rongcloud import RongCloud
APP_KEY = 'x4vkb1qpvxu4k'
APP_SECRET = 'EziWuNBddbcfz'
app_key = os.environ[APP_KEY]
app_secret = os.environ[APP_SECRET]
rcloud = RongCloud(app_key, app_secret)
r = rcloud.User.getToken(userId='userid1', name='username', portraitUri='http://www.rongcloud.cn/images/logo.png')
print(r)

print r
