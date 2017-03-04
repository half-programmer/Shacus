# -*- coding:utf-8  -*-
from BaseHandlerh import BaseHandler
from Database.models import get_db
from Database.tables import Appointment


class APgroupHandler(object):

    def GetGroupId(cls):
        retdata = []
        for x in range(5):
            apdata = {'type':'','apid':[]}
            ap=get_db().query(Appointment).filter(Appointment.APgroup == x+1).all()

            if x+1 == 1:
                apdata['type']='写真客片'
            elif x+1 == 2:
                apdata['type'] = '记录随拍'
            elif x+1 == 3:
                apdata['type'] = '练手互免'
            elif x+1 == 4:
                apdata['type'] = '活动跟拍'
            elif x+1 == 5:
                apdata['type'] = '商业拍摄'

            for item in ap:
                apdata['apid'].append(item.APid)
            retdata.append(apdata)
        return retdata
