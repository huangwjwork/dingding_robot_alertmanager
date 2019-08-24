from django.http import HttpResponse
import json
from api.log import logger
from api.dingtalk import query_dingtalk_api, post_dingtalk
from api.models import Alert, Receiver


# Create your views here.
def alert_data(request):
    if request.method == 'POST':
        receive_json_data = json.loads(request.body)
        # print(receive_json_data)
        receiver = receive_json_data['receiver']
        receivers = query_dingtalk_api(receiver)
        status = receive_json_data['status']
        for a in receive_json_data['alerts']:

            post_dingtalk(alert_json=a,
                          status=status,
                          dingtalk_robot_api=receivers[0])
            q1 = Alert.objects.filter(alertname=a['labels']['alertname'],
                                      instance=a['labels']['instance'],
                                      job=a['labels']['job'],
                                      receiver=receiver,
                                      startsAt=a['startsAt'])
            receivers = (list(receivers[1:]) + list(receivers[0])
                         if len(receivers) > 1 else receivers)

            if len(q1) == 0:
                alert = Alert(alertname=a['labels']['alertname'],
                              instance=a['labels']['instance'],
                              job=a['labels']['job'],
                              receiver=receiver,
                              startsAt=a['startsAt'],
                              endsAt=a['endsAt'],
                              status='firing',
                              post_times='1')
                alert.save()
            else:
                alert = q1[0]
                if status == 'firing':
                    alert.post_times += 1
                    alert.save()
                else:
                    alert.status = 'resolved'
                    alert.save()
        return HttpResponse("POST success")
    # except Exception as e:
    #     logger.error(e)

    else:
        return HttpResponse('forbidden')
