#-*- coding:-utf-8 -*-
def response(item,retdata):
    m_response=dict(
        ACid=item.ACid,
        ACsponsorid=item.ACsponsorid,
        AClocation=item.AClocation,
        ACtitle=item.ACtitle,
        ACtag=item.ACtag,
        ACstartT=item.ACstartT.strftime('%Y-%m-%dT%H:%M:%S'),
        ACendT=item.ACendT.strftime('%Y-%m-%dT%H:%M:%S'),
        ACjoinT=item.ACjoinT.strftime('%Y-%m-%dT%H:%M:%S'),
        ACcontent=item.ACcontent,
        ACfree=item.ACfree,
        ACprice=item.ACprice,
        ACclosed=item.ACclosed,
        ACcreateT=item.ACcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
        ACcommentnumber=item.ACcommentnumber,
        ACmaxp=item.ACmaxp,
        ACminp=item.ACminp,
        ACscore=item.ACscore,
        AClikenumber=item.AClikenumber,
        ACvalid=item.ACvalid,
    )
    retdata.append(m_response)

