from django.http import HttpResponse
import json
from api.dingtalk import query_dingtalk_api, post_dingtalk
from api.models import Alert, Receiver


# Create your views here.
def alert_data(request):
    if request.method == 'POST':
        # alertmanager json
        receive_json_data = json.loads(request.body)
        # print(receive_json_data)
        # 获取json中receiver
        receiver = receive_json_data['receiver']
        # 查询数据库中receiver dingtalk webhook列表
        receivers = query_dingtalk_api(receiver)
        # 获取告警状态 firing or resolved
        status = receive_json_data['status']
        # 遍历告警列表
        for a in receive_json_data['alerts']:
            # 发送告警信息，dingtalk接口为列表元素0
            post_dingtalk(alert_json=a,
                          status=status,
                          dingtalk_robot_api=receivers[0])
            # 将刚才发送过消息的接口移到列表最后一位，实现dingtalk接口轮询
            receivers = (receivers[1:] + [(receivers[0]]
                         if len(receivers) > 1 else receivers)
            # 查询当前告警是否在数据库
            q1 = Alert.objects.filter(alertname=a['labels']['alertname'],
                                      instance=a['labels']['instance'],
                                      job=a['labels']['job'],
                                      receiver=receiver,
                                      startsAt=a['startsAt'])
            # 数据库中不存在告警，则插入告警记录
            if len(q1) == 0:
                alert = Alert(alertname=a['labels']['alertname'],
                              instance=a['labels']['instance'],
                              job=a['labels']['job'],
                              receiver=receiver,
                              startsAt=a['startsAt'],
                              endsAt=a['endsAt'],
                              status=a['status'],
                              post_times='1')
                alert.save()
            # 数据库中存在告警，则判断告警状态
            else:
                alert = q1[0]
                # 状态为firing，重复告警，post_time+1
                if status == 'firing':
                    alert.post_times += 1
                    alert.save()
                # 状态为resolved，则将状态从firing置为resolved
                else:
                    alert.status = 'resolved'
                    alert.endsAt = a['endsAt']
                    alert.save()
        return HttpResponse("POST success")
    # except Exception as e:
    #     logger.error(e)

    else:
        return HttpResponse('<a href="/admin" >/admin/</a>')
