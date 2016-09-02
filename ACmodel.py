# coding=utf-8

def user_ac_simply(ac_info):
    ret_ac = {'acid': ac_info.ACid, 'acsponsorid': ac_info.ACsponsorid, 'actitle': ac_info.ACtitle,
              'aclocation': ac_info.AClocation, 'acvalid': ac_info.ACvalid,}
    return ret_ac