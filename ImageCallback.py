# -*-coding: utf-8 -*-
'''
@author: 兰威
'''


from BaseHandlerh import BaseHandler

class ImageCallback(BaseHandler):
    def post(self):
        print('\n---------headers\n')
        print (self.request.headers)