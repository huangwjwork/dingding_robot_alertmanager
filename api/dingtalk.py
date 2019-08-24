from api.models import Receiver
import requests
import json


def query_dingtalk_api(receiver):
    receivers = Receiver.objects.filter(receiver=receiver)
    api_list = []
    for i in receivers:
        api_list.append(i.dingtalk_robot_api)
    return api_list


def post_dingtalk(alert_json, status, dingtalk_robot_api):
    msg = ''
    msg = msg + '### %s  \n' % status
    for i in alert_json['labels']:
        msg = msg + '**%s:** %s  \n' % (i, alert_json['labels'][i])
    msg = msg + '**startsAt:** %s  \n' % alert_json['startsAt']
    if status == 'resolved':
        msg = msg + '**endsAt:** %s  \n' % alert_json['endsAt']
    for j in alert_json['annotations']:
        msg = msg + '**%s:** %s  \n' % (j, alert_json['annotations'][j])

    headers = {'Content-Type': 'application/json'}
    title = status + ' ' + alert_json['labels']['alertname']
    body = {"msgtype": "markdown", "markdown": {"title": title, 'text': msg}}
    req = requests.post(url=dingtalk_robot_api,
                        headers=headers,
                        data=json.dumps(body))
    print('钉钉POST状态', req)
