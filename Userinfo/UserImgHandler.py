#-*- coding:utf-8 -*-
import time

from Database.models import get_db
from Database.tables import User, UserHomepageimg, Image, UserCollection, UserCollectionimg
from FileHandler.Upload import AuthKeyHandler


class UserImgHandler(object):
    # 删除个人照片
    def delete_Homepage_image(self,list,uid):#
        try:
            db = get_db()
            userinfo = db.query(User).filter(User.Uid == uid).one()
            for imageitem in list:
                try:
                    deleteimage = db.query(UserHomepageimg).filter(UserHomepageimg.UHpicurl == imageitem,UserHomepageimg.UHuser==userinfo.Uid).one()
                    deleteimage.UHpicvalid = 0
                    db.commit()
                except Exception, e:
                    print e
                    print '没有找到删除的图片'+imageitem
        except Exception, e:
            print e
            print 'the user doesn\'t exsit'
    # 添加个人照片
    def insert_Homepage_image(self,list,uid):
        try:
            db = get_db()
            userinfo = db.query(User).filter(User.Uid == uid).one()
            for picurl in list:
                try:
                    isexist = db.query(UserHomepageimg).filter(UserHomepageimg.UHpicurl == picurl,UserHomepageimg.UHuser==userinfo.Uid).one()
                    isexist.UHpicvalid = 1
                    db.commit()
                except Exception, e:
                    # 单张图片插入
                    image = Image(
                        IMvalid=True,
                        IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                        IMname=picurl
                    )
                    db.merge(image)
                    db.commit()
                    new_img = get_db().query(Image).filter(Image.IMname == picurl).one()
                    imid = new_img.IMid
                    new_hpimg = UserHomepageimg(
                        UHuser=userinfo.Uid,
                        UHimgid=imid,
                        UHpicurl=picurl,
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
        for picurl in list:
            try:
                isexist = db.query(UserCollectionimg).filter(UserCollectionimg.UCIurl==picurl,UserCollectionimg.UCIuser == ucid).one()
                isexist.UHpicvalid = 1
                db.commit()
            except Exception, e:#未找到该图片
                print'插入单张新图片'
                image = Image(
                    IMvalid=True,
                    IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                    IMname=picurl
                )
                db.merge(image)
                db.commit()
                new_img = get_db().query(Image).filter(Image.IMname == picurl).one()
                imid = new_img.IMid
                new_ucimg=UserCollectionimg(
                    UCIuser=ucid,
                    UCIimid=imid,
                    UCIurl=picurl,
                    UCIvalid=1,
                )
                db.merge(new_ucimg)
                db.commit()

    def delete_UserCollection_image(self, list, ucid):
        # list:要删除的图片
        try:
            db = get_db()
            userinfo = db.query(UserCollection).filter(UserCollection.UCid == ucid).one()
            allimage = db.query(UserCollectionimg).filter(UserCollectionimg.UCIuser == userinfo.UCid).all()
            for imageitem in list:
                try:
                    deleteimage = db.query(UserCollectionimg).filter(UserCollectionimg.UCIurl == imageitem,
                                                                     UserCollectionimg.UCIuser == ucid).one()
                    deleteimage.UCIvalid = 0
                    db.commit()
                except Exception, e:
                    print e
                    print '没有找到删除的图片'+imageitem
            db.commit()

        except Exception, e:
            print e
            print 'the usercollection doesn\'t exsit'


    # 得到个人照片大图
    def UHpicget(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid).all()  # 返回所有图片项
        for img in imgs:
            img_url = img.UHpicurl
            img_tokens.append(authkeyhandler.download_originpic_url(img_url)) # 裁剪？1200宽度
        if img_tokens[0]:
                print '有图片'
        else:
            img_tokens = []
        return img_tokens

    # 得到个人照片缩略图
    def UHpicgetassign(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid).all()  # 返回所有图片项

        if imgs[0].UHpicurl:
            print '有图片'
            for img in imgs:
                img_url = img.UHpicurl
                img_size = authkeyhandler.getsize(img_url)
                img_info = dict(
                    imageUrl=authkeyhandler.download_abb_url(img_url),
                    width=img_size['width']/6,
                    height=img_size['height']/6,
                )
                img_tokens.append(img_info)
        else:
            img_tokens.append('null')
        return img_tokens

    # b->c作品集详细信息(包括缩略图url和大图url)
    def UCmodel(self,UCsample,uid):  # UCsample是一个UserCollection对象
        authkeyhandler = AuthKeyHandler()
        img = []
        imgsimple = []
        ucimg = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid).all()
        for item in ucimg:
            ucimgurl = item.UCIurl
            img.append(authkeyhandler.download_originpic_url(ucimgurl))   # 大图url

            #img_size = authkeyhandler.getsize(ucimgurl)   # 获取图片json对象
            img_info = dict(
                imageUrl=authkeyhandler.download_abb_url(ucimgurl),
                #width=img_size['width'] / 6,
                #height=img_size['height'] / 6,
                width='200',
                height='123'
            )
            imgsimple.append(img_info)
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCuser=uid,
            UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d %H:%M:%S'),
            UCtitle=UCsample.UCtitle,
            UCcontent=UCsample.UCcontent,
            UCimg=img,                  # 大图url
            UCsimpleimg=imgsimple,      # 缩略图url
        )
        return ret_uc

    # a->b:作品集列表:某个列表封面的获取
    def UC_simple_model(self,UCsample,uid):
        authkeyhandler = AuthKeyHandler()
        # ucsample是一个UserCollection实例
        ucimg = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid).all()
        if ucimg:
            coverurl = authkeyhandler.download_abb_url(ucimg[0].UCIurl)   # 选取第一张作为封面(缩略图)
            img_size = authkeyhandler.getsize(ucimg[0].UCIurl)
            img_info = dict(
                imageUrl=coverurl,
                width=img_size['width'] / 6,
                height=img_size['height'] / 6,
            )
        else:
            img_info = dict(
                imageUrl='',
            )
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d %H:%M:%S'),
            UCimg=img_info,
        )
        return ret_uc

    # a:个人主页作品集封面
    def UC_homepage_model(self, ucsample, uid):
        print ''
