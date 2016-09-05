#-*- coding:-utf-8 -*-
from tokenize import String


def response(item,retdata,url):#查看活动更多详情
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
        ACfree=int(item.ACfree),
        ACprice=item.ACprice,
        ACclosed=int(item.ACclosed),
        ACcreateT=item.ACcreateT.strftime('%Y-%m-%dT%H:%M:%S'),
        ACcommentnumber=item.ACcommentnumber,
        ACmaxp=item.ACmaxp,
        ACminp=item.ACminp,
        ACscore=item.ACscore,
        AClikenumber=item.AClikenumber,
        ACvalid=int(item.ACvalid),
        ACstatus = item.ACstatus,
        ACimageurl = url
    )
    retdata.append(m_response)


def Acresponse(item,item2,retdata):

    m_Acresponse=dict(
        ACid=item.ACid,
        ACsponsorid=item.ACsponsorid,#username
        AClocation=item.AClocation,#location
        ACcontent=item.ACcontent,#
        ACstartT=item.ACstartT.strftime('%Y-%m-%dT%H:%M:%S'),#settime
        AClikenumber=item.AClikenumber,#praisenum
        ACregistN=item.ACregistN,#joinnum
        AClurl="http://img4.imgtn.bdimg.com/it/u=1293975569,236516549&fm=21&gp=0.jpg#token",
        Userimageurl="http://img4.imgtn.bdimg.com/it/u=2898602429,470889281&fm=21&gp=0.jpg",
        Ualais=item2.Ualais,
    )
    retdata.append(m_Acresponse)

