# -*- coding: utf-8 -*-
#!/usr/bin/env python
import tornado.httpserver
import  tornado.ioloop
import  tornado.options
import tornado.web
from APHandler import APcreateHandler, APaskHandler, APregistHandler
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options
from Database.models import engine
from RegisterHandler import RegisterHandler
from ImageCallback import ImageCallback
from loginHandler import LoginHandler
from ACHandler import ActivityCreate

define("port", default=800, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
             (r"/appointment/create", APcreateHandler),
             (r"/appointment/ask", APaskHandler),
             # (r"/appointment/ask", AskAppointment),
             # (r"/appointment/register", RegistAppointment),
             (r"/login", LoginHandler),
             (r"/regist", RegisterHandler),
              (r"/activity/create", ActivityCreate),
             # (r"/Activity/ask", AskActivity),
             # (r"/Activity/register", ActivityJoin),
             (r"/ImageCallback",ImageCallback)

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

