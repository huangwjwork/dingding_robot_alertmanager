from api.models import Receiver
import requests
import json
import re


# 查询receiver信息，取出webhook，并保存为list
def query_dingtalk_api(receiver):
    receivers = Receiver.objects.filter(receiver=receiver)
    api_list = []
    for i in receivers:
        api_list.append(i.dingtalk_robot_api)
    return api_list


# 将告警json格式化为Markdown并发送到dingtalk，若模板出错则采用默认格式化发送
def post_dingtalk(alert_json, status, dingtalk_robot_api, template, key_words):
    try:
        msg = template
        # 根据变量名按条件替换变量
        for key_word in key_words:
            if key_word in ['status', 'startsAt', 'endsAt', 'generatorURL']:
                msg = msg.replace('{$%s}' % key_word, alert_json[key_word])
            elif key_word in ['description', 'summary']:
                msg = msg.replace('{$%s}' % key_word,
                                  alert_json['annotations'][key_word])
            else:
                msg = msg.replace('{$%s}' % key_word,
                                  alert_json['labels'][key_word])
    except Exception as e:
        print(e)
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
