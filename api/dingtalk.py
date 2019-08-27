from api.models import Receiver
import requests
import json


# 查询receiver信息，取出webhook，并保存为list
def query_dingtalk_api(receiver):
    receivers = Receiver.objects.filter(receiver=receiver)
    api_list = []
    for i in receivers:
        api_list.append(i.dingtalk_robot_api)
    return api_list


# 将告警json格式化为Markdown并发送到dingtalk
def post_dingtalk(alert_json, status, dingtalk_robot_api):
    msg = ''
    msg = msg + '### %s  \n' % status
    # 获取alert json的labels
    for i in alert_json['labels']:
        msg = msg + '**%s:** %s  \n' % (i, alert_json['labels'][i])
    # 开始时间
    msg = msg + '**startsAt:** %s  \n' % alert_json['startsAt']
    # 状态为resolved时，获取结束时间
    if status == 'resolved':
        msg = msg + '**endsAt:** %s  \n' % alert_json['endsAt']
    # 获取annotation
    for j in alert_json['annotations']:
        msg = msg + '**%s:** %s  \n' % (j, alert_json['annotations'][j])
    # 推送dingtalk
    headers = {'Content-Type': 'application/json'}
    title = status + ' ' + alert_json['labels']['alertname']
    body = {"msgtype": "markdown", "markdown": {"title": title, 'text': msg}}
    req = requests.post(url=dingtalk_robot_api,
                        headers=headers,
                        data=json.dumps(body))
    print('钉钉POST状态', req)
