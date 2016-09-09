# coding=utf-8
'''
@author :兰威
@type ： 用于获得用户聊天时的token
'''
import os

import requests

from rongcloud import RongCloud




APP_KEY = '8w7jv4qb78xsy'
APP_SECRET = 'FAYlYR9tz4Hiu'
app_key = os.environ[APP_KEY]
app_secret = os.environ[APP_SECRET]
p= RongCloud(app_key, app_secret)

r= p.User.getToken(
    userId= 100,
    name = 'lanwei'
)

print r
