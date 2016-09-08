# -*- coding: utf-8 -*-

def TRresponse(item,url,retdata):
    m_trresponse = dict (
        Tid=item.Tid,
        Tsponsorid=item.Tsponsorid,
        TsponsT=item.TsponsT.strftime('%Y-%m-%dT%H:%M:%S'),
        TcommentN=item.TcommentN,
        TlikeN=item.TlikeN,
        Tcontent=item.Tcontent,
        Ttitle=item.Ttitle,
        TIimgurl=url,
    )
    retdata.append(m_trresponse)