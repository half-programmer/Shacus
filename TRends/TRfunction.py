# -*- coding: utf-8 -*-
from FileHandler.Upload import AuthKeyHandler
def TRresponse(item,url,retdata):
    authkey= AuthKeyHandler()
    m_trresponse = dict (
        Tid=item.Tid,
        Tsponsorid=item.Tsponsorid,
        TsponsT=item.TsponsT.strftime('%Y-%m-%dT%H:%M:%S'),
        TcommentN=item.TcommentN,
        TlikeN=item.TlikeN,
        Tcontent=item.Tcontent,
        Ttitle=item.Ttitle,
        Tsponsorimg = item.Tsponsorimg,
        TIimgurl=authkey.download_url(url),
    )
    retdata.append(m_trresponse)