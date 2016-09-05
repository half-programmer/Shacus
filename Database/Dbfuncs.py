# -*- coding: utf-8 -*-

class Dbfuncs(object):

    @staticmethod
    def commit_error(self, retjson, e):
        '''
        Args:
            retjson: 修改的json
            e: 异常
        '''
        retjson['contents'] = '数据库更新错误'
        retjson['code'] = '10274'