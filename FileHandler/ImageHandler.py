# -*- coding: utf-8 -*-
import time

from BaseHandlerh import BaseHandler
from Database.tables import UserImage,Image,AppointmentImage,ActivityImage
'''
 创建者：黄鑫晨
 创建时间：2016-08-30 18:05
'''
class ImageHandler(BaseHandler):
    #def __init__(self):
    def insert(self,list):
        '''
        向数据库插入图片链接
        :param list: 图片名的列表
        :table: 应该插入的表名
        :return:
        '''
        new_imids=[]
        for img_name in list:  # 第一步，向Image里表里插入
            image = Image(
                IMvalid=True,
                IMT=time.strftime('%Y-%m-%dT%H:%M:%S')
            )
            self.db.merge(image)
            self.db.commit()
            new_img = self.db.query(Image).filter(Image.IMname == img_name).one()
            imid = new_img.IMid
            imgs.append(new_img)

    def insert_user_image(self, list, user):
                 '''
                 :param list: 图片名的列表
                 :param user: 发布该约拍的用户
                 :return:
                 '''

            for img_name in list:
                image = UserImage(
                    UIuid=user.Uid,
                    UIimid=
            )
                self.db.merge(image)
                self.db.commit()







                     #print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# timen = time.strftime('%Y-%m-%dT%H:%M:%S')
# timeStamp = int(time.mktime(timen))
# print timeStamp