# coding=utf-8
class ACmodelHandler:
    @classmethod
    def ac_Model_simply(clas,activity):
        '''得到简单活动模型
        :return:  retjson
        '''
        #todo:查找待变更为最新10个

        ac_simply_info = dict(
        ACid=activity.ACid,
        ACtitle=activity.ACtitle,
        ACimgurl='暂无',
        ACstartT=activity.ACstartT.strftime('%Y-%m-%d %H:%M:%S'),
        AClikeN=activity.AClikenumber,
        ACregistN=activity.ACregistN
        )
        return ac_simply_info

