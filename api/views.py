from django.http import HttpResponse
import json
from api.alert import Alert


# Create your views here.
def alert_data(request):
    if request.method == 'POST':
        receive_json_data = json.loads(request.body)
        # print(receive_json_data)
        receiver = receive_json_data['receiver']
        status = receive_json_data['status']
        for a in receive_json_data['alerts']:
            alert = Alert(alert_json=a, receiver=receiver)
            alert.post_dingding()
            q1 = alert.query_alert(alert_status='firing')
            if len(q1) == 0:
                alert.insert_alert()
            else:
                if status == 'firing':
                    alert.update_alert_times()
                else:
                    alert.resolved_alert()
        return HttpResponse("POST success")
    else:
        return HttpResponse('forbidden')
