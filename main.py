# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.httpserver
import  tornado.ioloop
import  tornado.options
import tornado.web
from Activity.ACentryHandler import AskEntry
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options
from Activity.ACHandler import ActivityCreate, ActivityRegister
from Activity.ACaskHandler import AskActivity
from Appointment.APAskHandler import APaskHandler
from Appointment.APCreateHandler import APcreateHandler
from Appointment.APRegistHandler import APregistHandler
from Database.models import engine
from ImageCallback import ImageCallback
from RegisterHandler import RegisterHandler
from Userhomepager import Userhomepager
from Userinfo.UserIndent import UserIndent
from Userinfo.UserFavoriteHandler import UserFavorite
from Userinfo.UserLike import FindUlike
from loginHandler import LoginHandler
from Settings import PaswChange
from Userinfo.UserInfo import UserInfo

define("port", default=800, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
             (r"/appointment/create", APcreateHandler),
             (r"/appointment/ask", APaskHandler),
             (r"/appointment/regist", APregistHandler),
             (r"/login", LoginHandler),
             (r"/regist", RegisterHandler),
             (r"/user/homepager",Userhomepager),
             (r"/user/mylike", FindUlike),
             (r"/user/favorite", UserFavorite),
             (r"/user/info",UserInfo),
             (r"/user/indent",UserIndent),
             (r"/Activity/ask", AskActivity),
             (r"/Activity/entry", AskEntry),
             (r"/activity/create", ActivityCreate),
             (r"/activity/register",ActivityRegister),
             (r"/ImageCallback",ImageCallback),
            (r"/PaswChange",PaswChange)
        ]
        tornado.web.Application.__init__(self, handlers)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

# session负责执行内存中的对象和数据库表之间的同步工作 Session类有很多参数,使用sessionmaker是为了简化这个过程
if __name__ == "__main__":
    print "HI,I am in main "
    tornado.options.parse_command_line()
    Application().listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

