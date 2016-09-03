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
                IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                IMname = img_name
            )
            self.db.merge(image)
            self.db.commit()
            new_img = self.db.query(Image).filter(Image.IMname == img_name).one()
            imid = new_img.IMid
            new_imids.append(imid)
            return new_imids

    def insert_user_image(self, list, uid):
        '''

        Args:
            list:图片名字的数组
            uid: 用户的ID

        Returns:

        '''

        imids = self.insert(list)
        for i in range(len(imids)):
            image = UserImage(
                UIuid=uid,
                UIimid=imids[i],
                UIurl=list[i]
            )
        self.db.merge(image)
        self.db.commit()

    def insert_activity_image(self,list,ac_id):
        '''

        Args:
            list: 图片的名字的数组
            ac_id: 活动的ID

        Returns:

        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = ActivityImage(
                ACIacid=ac_id,
                ACIimid=imids[i],
                ACIurl=list[i]
            )
        self.db.merge(image)
        self.db.commit()

    def insert_appointment_image(self,list,ap_id):
        '''

        Args:
            list: 图片名字的数组
            ap_id: 约拍的ID


        Returns:

        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = AppointmentImage(
                APIacid=ap_id,
                APIimid=imids[i],
                APIurl=list[i]
            )
        self.db.merge(image)
        self.db.commit()










                     #print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# timen = time.strftime('%Y-%m-%dT%H:%M:%S')
# timeStamp = int(time.mktime(timen))
# print timeStamp