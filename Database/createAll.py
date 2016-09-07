# -*- coding: utf-8 -*-

#from Database.models import Base

from models import Base
from models import engine
import tables
Base.metadata.create_all(engine)
print "创建表"