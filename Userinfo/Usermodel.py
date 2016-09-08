# coding=utf-8
from Database.models import get_db
from Database.tables import UserImage
from FileHandler.Upload import AuthKeyHandler


def userinfo_smply(u_info, u_change_info):
    '''

    Args:
        u_info:
        u_change_info:
    返回个人简单信息
    Returns:

    '''
    ret_info = {'uid': u_info.Uid, 'ualais': u_info.Ualais, 'ulocation': u_info.Ulocation,
                     'utel': u_info.Utel, 'uname': u_info.Uname, 'umailbox': u_info.Umailbox,
                     'ubirthday': u_info.Ubirthday, 'uscore': u_info.Uscore, 'usex': u_info.Usex,
                     'usign': u_info.Usign, 'uimage': '', 'ulikeN': u_change_info.UClikeN,
                     'ulikedN': u_change_info.UClikedN, 'uapN': u_change_info.UCapN,
                     'uphotoN': u_change_info.UCphotoN, 'ucourseN': u_change_info.UCcourseN,
                     'umomentN': u_change_info.UCmomentN}
    return ret_info

def Model_daohanglan(imgurl,weburl):
    dh_json = {'imgurl':imgurl, 'weburl':weburl}
    return dh_json

def user_login_fail_model():
    user_model = dict(
        id='0',
        phone='wu',
        nickName='wu',
        realName='wu',
        sign='wu',
        sex='wu',
        score='wu',
        location='wu',
        birthday='wu',
        registTime='wu',
        mailBox='wu',
        headImage='wu',
        auth_key='wu'
    )
    return user_model

