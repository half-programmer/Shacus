# -*- coding:utf-8 -*-
def ApInforesponse(item,retdata):
    m_ApInforesponse=dict(
        AIid=item.AIid,
        AImid=item.AImid,
        AIpid=item.Aipid,
        AImscore=item.AImscore,
        AIpscore=item.AIpscore,
        AImcomment=item.AImcomment,
        AIpcomment=item.AIpcomment,
        AIappoid=item.AIappoid
    )
    retdata.append(m_ApInforesponse)

def ApUserinfo(item,retdata):
    m_ApUserinfo=dict(
    Uid=item.Uid, # 主键
    Upassword =item.Upassword,
    Utel =item.Utel,
    Ualais =item.Ualais,
    Uname =item.Uname, # 真实姓名
    Ulocation = item.Ulocation,
    Umailbox = item.Umailbox,

    Ubirthday =item.Ubirthday.strftime('%Y-%m-%dT%H:%M:%S'),
    Uscore = item.Uscore,
    UregistT =item.UregistT.strftime('%Y-%m-%dT%H:%M:%S'),
    Usex = item.Usex,
    Usign = item.Usign,
    Uauthkey = item.Uauthkey
    )
    retdata.append(m_ApUserinfo)


def APinfochoose(item,item2,retdata):
    m_APinfochoose=dict(
        Uid=item.Uid,
        Usign=item.Usign,
        Ualais=item.Ualais,
        UIurl=item2.UIurl,
    )
    retdata.append(m_APinfochoose)

