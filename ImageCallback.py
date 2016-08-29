# -*-coding: utf-8 -*-

__author__='lanwei'

from BaseHandlerh import BaseHandler

class ImageCallback(BaseHandler):
    def post(self):
        print('\n---------headers\n')
        print (self.request.headers)