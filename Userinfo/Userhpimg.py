# coding=utf-8
# 个人主页图片：包括个人照片和作品集
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, UserHomepageimg, UserCollection
from FileHandler.ImageHandler import ImageHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo.UserImgHandler import UserImgHandler


class Userhpimg(BaseHandler):
    retjson = {'code': '', 'contents': ""}
    def post(self):
        type = self.get_argument('type')

        if type=='10808': #个人图片
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid==u_id).one()
                key = userid.Uauthkey
                if key== auth_key:  #验证通过
                    print '验证通过'
                    ap_imgs_json = json.loads(imgs)
                    retjson_body = {'auth_key': '', 'uid': ''}
                    auth_key_handler = AuthKeyHandler()
                    retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)#上传凭证
                    #插入数据库

                    retjson_body['uid']= userid.Uid
                    self.retjson['contents'] = retjson_body
                    self.retjson['code']= '10808'


            except Exception, e:
                print e
                self.retjson['code']='10809'
                self.retjson['contents']='验证失败'

        elif type == '10810':
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid==u_id).one()
                key = userid.Uauthkey
                if key== auth_key:  #验证通过
                    print '验证通过'
                    ap_imgs_json = json.loads(imgs)
                    imhandler= UserImgHandler()
                    imhandler.delete_Homepage_image(u_id)
                    imhandler.change_Homepage_image(ap_imgs_json,u_id)
                    self.retjson['code']= '10810'
                    self.retjson['contents'] = '数据库操作成功'
                else:
                    print '验证码错误'
                    self.retjson['code'] = '10811'
                    self.retjson['contents'] = '验证未通过'
            except Exception, e:
                print e
                self.retjson['code']='10811'
                self.retjson['contents']='查找用户失败'

        elif type == '10812':#获取个人图片
            uhuser = self.get_argument('uid')
            authkey = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid == uhuser).one()
                key = userid.Uauthkey
                if key == authkey:  # 验证通过
                    img= UserImgHandler()
                    piclist = img.UHpicget(uhuser)
                    self.retjson['code']='10812'
                    self.retjson['contents']= piclist
                else:
                    print'认证错误'
                    self.retjson['code']='10813'
                    self.retjson['contents']= '用户认证错误'
            except Exception, e:
                print e
                self.retjson['code']='10813'
                self.retjson['contents']='未找到该用户'
        elif type == '10814':#获取个人图片缩略图
            uhuser = self.get_argument('uid')
            authkey = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid == uhuser).one()
                key = userid.Uauthkey
                if key == authkey:  # 验证通过
                    img= UserImgHandler()
                    piclist = img.UHpicgetassign(uhuser)
                    self.retjson['code']='10814'
                    self.retjson['contents']= piclist
                else:
                    print'认证错误'
                    self.retjson['code']='10815'
                    self.retjson['contents']= '用户认证错误'
            except Exception, e:
                print e
                self.retjson['code']='10815'
                self.retjson['contents']='未找到该用户'



        elif type=='10804' :#作品集
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            uc_title = self.get_argument('title')
            try:
                userid = self.db.query(User).filter(User.Uid==u_id).one()
                key = userid.Uauthkey
                if key== auth_key:  #验证通过
                    print '验证通过'
                    ap_imgs_json = json.loads(imgs)
                    retjson_body = {'auth_key': '', 'ucid': ''}
                    auth_key_handler = AuthKeyHandler()
                    retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)  # 上传凭证
                    # 插入数据库
                    try:
                        new_usercollection = UserCollection(
                            UCuser=u_id,
                            UCtitle=uc_title,
                            UCcontent='',
                            UCvalid=0,
                            UCiscollection=0,
                        )
                        self.db.merge(new_usercollection)
                        self.db.commit()
                    except Exception,e :
                        print e
                        self.retjson['contents']='数据库插入失败'
                    try:
                        print '插入成功，进入查询'
                        uc = self.db.query(UserCollection).filter(
                           UserCollection.UCtitle == uc_title, UserCollection.UCuser == u_id).one()
                        ucid = uc.UCid
                        retjson_body['ucid'] = ucid
                        self.retjson['contents'] = retjson_body
                        self.retjson['code']='10804'
                    except Exception, e:
                        print '插入失败！！'
                        self.retjson['contents'] = r'服务器插入失败'
                else:
                    self.retjson['code']= '10805'
                    self.retjson['contents']= '用户认证失败'
            except Exception, e:
                    print e
                    self.retjson['code'] = '10805'
                    self.retjson['contents'] = "该用户名不存在"

        elif type == '10806':
            print "进入10806"
            uc_id = self.get_argument('ucid')
            auth_key = self.get_argument('authkey')
            ap_title = self.get_argument('title')
            uc_content = self.get_argument('content')
            uc_imgs = self.get_argument('imgs')
            try:

                self.db.query(UserCollection).filter(UserCollection.UCid == uc_id).\
                                    update({ UserCollection.UCcontent: uc_content,
                                             UserCollection.UCvalid: 1,
                                             UserCollection.UCtitle:ap_title,
                                            }, synchronize_session=False)
                self.db.commit()
                print '更新完成'
                try:
                    imghandler = UserImgHandler()
                    uc_images_json=json.loads(uc_imgs)
                    imghandler.insert_UserCollection_image(uc_images_json,uc_id)
                    self.db.commit()
                    self.retjson['code'] = '10806'
                    self.retjson['contents'] = '发布作品集成功'
                except Exception, e:
                    print e
                    self.retjson['code']='10807'
                    self.retjson['contents'] = u'插入图片表失败'
            except Exception, e:
                print e

        elif type == '10816':#获取作品集缩略图和标题
            u_id = self.get_argument('uid')
            auth_key = self.get_argument("authkey")
            imghandler = UserImgHandler()
            retdata = []
            pic = self.db.query(UserCollection).filter(UserCollection.UCuser == u_id).all()
            for item in pic:
                retdata.append(imghandler.UC_simple_model(item, u_id))
            self.retjson['code'] = '10818'
            self.retjson['contents'] = retdata

        elif type == '10818':
            print ''
            u_id = self.get_argument('uid')
            auth_key = self.get_argument("authkey")
            imghandler=UserImgHandler()
            retdata= []
            pic = self.db.query(UserCollection).filter(UserCollection.UCuser==u_id).all()
            for item in pic:
                retdata.append(imghandler.UCmodel(item,u_id))
            self.retjson['code']='10818'
            self.retjson['contents']=retdata
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

