# coding=utf-8

def response(item, retdata):

        m_response = dict(
            activityID=item.activityID,
            sponsorID=item.sponsorID,
            activity_name=item.activity_name,
            activity_introduction=item.activity_introduction,
            type=item.type,
            location=item.location,
            start_time=item.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            end_time=item.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            min_people=item.min_people,
            max_people=item.max_people,
            closed=item.closed,
            imageurl=item.imageurl
        )
        retdata.append(m_response)