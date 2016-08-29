# -*- coding: utf-8 -*-

from models import Base
import tables
#from models import Base
from models import engine
Base.metadata.create_all(engine)
print "创建表"