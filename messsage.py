# -*- coding:utf-8 -*-


import sys, urllib, urllib2, json
def message(code=000000,phone=00000000000):
   url = "http://imlaixin.cn/Api/send/data/json?accesskey=5025&secretkey=754c1c14fdda4935c127af9d9331447ed752de97&mobile="+phone+"&content=尊敬的用户您好，您的验证码为："+code+"，请不要告诉别人哦！【Vita】"
   req = urllib2.Request(url)
   resp = urllib2.urlopen(req)
   str = resp.read()
   if(str):
       print(str)