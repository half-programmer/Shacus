# coding=utf-8

def userinfo_smply(u_info,u_change_info):
    ret_info = {'uid': u_info.Uid, 'ualais': u_info.Ualais, 'ulocation': u_info.Ulocation,
                     'utel': u_info.Utel, 'uname': u_info.Uname, 'umailbox': u_info.Umailbox,
                     'ubirthday': u_info.Ubirthday, 'uscore': u_info.Uscore, 'usex': u_info.Usex,
                     'usign': u_info.Usign, 'uimage': '', 'ulikeN': u_change_info.UClikeN,
                     'ulikedN': u_change_info.UClikedN, 'uapN': u_change_info.UCapN,
                     'uphotoN': u_change_info.UCphotoN, 'ucourseN': u_change_info.UCcourseN,
                     'umomentN': u_change_info.UCmomentN}
    return ret_info