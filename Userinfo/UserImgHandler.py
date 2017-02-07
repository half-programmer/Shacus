#-*- coding:utf-8 -*-
import time

from Database.models import get_db
from Database.tables import User, UserHomepageimg, Image, UserCollection, UserCollectionimg
from FileHandler.Upload import AuthKeyHandler


class UserImgHandler(object):
    def delete_Homepage_image(self,uid):#先注释掉该用户的所有图片

        try:
            db = get_db()
            userinfo = db.query(User).filter(User.Uid == uid).one()
            allimage=  db.query(UserHomepageimg).filter(UserHomepageimg.UHuser == userinfo.Uid).all()
            for item in allimage:
                item.UHpicvalid = 0
            db.commit()

        except Exception, e:
            print e
            print 'the user doesn\'t exsit'

    def change_Homepage_image(self,list,uid):#改变个人图片信息
        try:
            db = get_db()
            for item in list:  #如果有那么重置为1，如果没有就继续保持0
                try:
                    userimage = db.query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid,UserHomepageimg.UHpicurl == item).one()
                    userimage.HPimgvalid = 1
                    db.commit()
                except Exception ,e:#新的需要插入
                    print 'insert new Homepageimage'
                    itemlist = []
                    itemlist.append(item)
                    self.insert_Homepage_image(itemlist, uid)
        except Exception,e:
            print e
            print 'doesn\'t exsit'

    def insert_Homepage_image(self,list,uid):
        try:
            db = get_db()
            usertel = db.query(User).filter(User.Uid == uid).one()
            HPimg = self.insert(list)

            for i in range(len(HPimg)):
                new_hpimg = UserHomepageimg(

                    UHuser=usertel.Uid,
                    UHimgid=HPimg[i],
                    UHpicurl=list[i],
                    UHpicvalid=True,
                )
                db.merge(new_hpimg)
                db.commit()
        except Exception, e:
            print e


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
            db=get_db()
            db.merge(image)
            db.commit()
            new_img = get_db().query(Image).filter(Image.IMname == img_name).one()
            imid = new_img.IMid
            new_imids.append(imid)
        return new_imids

    def insert_UserCollection_image(self,list,ucid):
        db = get_db()
        itemlist=[]
        for item in list:
            itemlist.append(item)
        try:
            HPimg = self.insert(itemlist)
            for i in range(len(HPimg)):
                new_ucimg=UserCollectionimg(
                    UCIuser=ucid,
                    UCIimid=HPimg[i],
                    UCIurl=itemlist[i],
                    UCIvalid=1,
                )
                db.merge(new_ucimg)
                db.commit()
        except Exception, e:
            print e

    def delete_UserCollection_image(self,list,ucid):
        db = get_db()
        itemlist = []
        for item in list:
            itemlist.append(item)

    #得到图片
    def UHpicget(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        try:
            imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid).all()  # 返回所有图片项
            for img in imgs:
                img_url = img.UHpicurl
                img_tokens.append(authkeyhandler.download_url(img_url))
        except Exception, e:
            print '无图片'
        try:
            if img_tokens[0]:
                print '有图片'
        except Exception, e:
            img_tokens.append(authkeyhandler.download_url('default13.jpg'))
            print e
        return img_tokens

    def UHpicgetassign(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        try:
            imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid).all()  # 返回所有图片项
            for img in imgs:
                img_url = img.UHpicurl
                img_tokens.append(authkeyhandler.download_assign_url(img_url,1200,1200))
        except Exception, e:
            print '无图片'
        try:
            if img_tokens[0]:
                print '有图片'
        except Exception, e:
            img_tokens.append(authkeyhandler.download_url('default13.jpg'))
            print e
        return img_tokens

    def UCmodel(self,UCsample,uid):#UCsample是一个UserCollection对象
        authkeyhandler = AuthKeyHandler()
        img = []
        ucimg = self.db.query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid).all()
        for item in ucimg:
            ucimgurl = item.UCIurl
            img.append(authkeyhandler.download_url(ucimgurl))
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCuser=uid,
            UCcreateT=UCsample.UCcreateT,
            UCtitle=UCsample.UCtitle,
            UCcontent=UCsample.UCcontent,
            UCimg=img,
        )
        return ret_uc
    def UC_simple_model(self,UCsample,uid):
        authkeyhandler = AuthKeyHandler()
        img = []
        ucimg = self.db.query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid).all()
        for item in ucimg:
            ucimgurl = item.UCIurl
            img.append(authkeyhandler.download_assign_url(ucimgurl,1200,1200))
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCimg=img,
        )


