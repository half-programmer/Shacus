# coding=utf-8

def response(data, retdata):

    for item in data:
        m_response = dict(
            appointmentID=item.appointmentID,
            sponsorID=item.sponsorID,  # 发起者
            appointment_name=item.appointment_name,
            appointment_introduction=item.appointment_introduction,
            self_introduction=item.self_introduction,
            location=item.location,
            styleID=item.styleID,
            start_time=item.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            end_time=item.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            closed=item.closed,
            imageurl=item.imageurl
        )
        retdata.append(m_response)