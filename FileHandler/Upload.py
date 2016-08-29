# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

#需要填写的 Access Key 和 Secret Key
access_key = 'yzAza_Cm87nXkh9IyFfpg7LL7qKJ097VK5IOpLj0'
secret_key = 'GFWHU9hYkU4hepDwpWfHaNDt3gJCDsAk3Kz6DGdk'

#构建鉴权对象
Auth_key = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'shacus'

#上传到七牛后保存的文件名
key = '20160829.jpg'


#生成上传 Token，可以指定过期时间等
auth_token = Auth_key.upload_token(bucket_name, key, 3600)
#print auth_token


# todo 封装auth_token
# class AuthKeyHandler:
#     auth_token = Auth_key.upload_token(bucket_name, key, 3600)
#     @property
#     def Authkey(self):
#         return Auth_key
#
#     @property
#     def token(self):
#         print  self.auth_token
#         return self.auth_token
#
# print  AuthKeyHandler.token
