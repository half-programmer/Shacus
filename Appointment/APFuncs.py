# coding=utf-8

def response(data, retdata):

    for item in data:
        m_response = dict(
            APid=item.APid,
            APtitle=item.APtitle,
            APsponsorid=item.APsponsorid,
            APtag=item.APtag,
            APtype=item.APtype,
            APlocation=item.APlocation,
            APstartT=item.APstartT.strftime('%Y-%m-%dT%H:%M:%S'),
            APendT=item.APendT.strftime('%Y-%m-%dT%H:%M:%S'),
            APjoinT=item.APjoinT.strftime('%Y-%m-%dT%H:%M:%S'),
            APcontent=item.APcontent,
            APfree=item.APfree,
            APprice=item.APprice,
            APclosed=item.APclosed,
            APcreateT=item.APcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
            APaddallowed=item.APaddallowed,
            APlikeN=item.APlikeN,
            APvalid=item.APvalid
        )
        retdata.append(m_response)