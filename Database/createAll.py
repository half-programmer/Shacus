# -*- coding: utf-8 -*-

from Database.models import Base

#from models import Base

#import tables
from models import engine
import Database.tables

Base.metadata.create_all(engine)
print "创建表"