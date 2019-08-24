import json
import requests
from api.models import Alert_info
from api.models import Receiver
import datetime


def format_time(t):
    t = t[0:26] + 'Z'
    t.replace(' ', 'T', 1)
    return t


class Alert(object):
    def __init__(self, alert_json, receiver):
        self._alert_json = alert_json
        self._receiver = receiver
        self.startsAt = format_time(self._alert_json['startsAt'])
        # self.endsAt = format_time(self._alert_json['endsAt'])

    def get_webhook_url(self):
        return Receiver.objects.get(receiver=self._receiver).dingding_robot_api

    def post_dingding(self):
        msg = ''
        status = self._alert_json['status']
        msg = msg + '### %s  \n' % status
        for i in self._alert_json['labels']:
            msg = msg + '**%s:** %s  \n' % (i, self._alert_json['labels'][i])
        msg = msg + '**startsAt:** %s  \n' % self._alert_json['startsAt']
        if status == 'resolved':
            msg = msg + '**endsAt:** %s  \n' % self._alert_json['endsAt']
        headers = {'Content-Type': 'application/json'}
        title = status + ' ' + self._alert_json['labels']['alertname'] 
        body = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                'text': msg
            }
        }
        webhook_url = self.get_webhook_url()
        req = requests.post(url=webhook_url,
                            headers=headers,
                            data=json.dumps(body))
        print('钉钉POST状态', req)

    def query_alert(self, alert_status):
        query_list = Alert_info.objects.filter(
            alertname=self._alert_json['labels']['alertname'],
            instance=self._alert_json['labels']['instance'],
            job=self._alert_json['labels']['job'],
            monitor=self._alert_json['labels']['monitor'],
            severity=self._alert_json['labels']['severity'],
            startsAt=self.startsAt,
            receiver=self._receiver,
            status=alert_status)
        return query_list

    def insert_alert(self):
        i = Alert_info(alertname=self._alert_json['labels']['alertname'],
                       instance=self._alert_json['labels']['instance'],
                       job=self._alert_json['labels']['job'],
                       monitor=self._alert_json['labels']['monitor'],
                       severity=self._alert_json['labels']['severity'],
                       startsAt=self.startsAt,
                       endsAt=self._alert_json['endsAt'],
                       receiver=self._receiver,
                       status='firing',
                       post_times=1)
        i.save()

    def update_alert_times(self):
        a1 = self.query_alert(alert_status='firing')[0]
        a1.post_times += 1
        a1.save()

    def resolved_alert(self):
        r1 = self.query_alert(alert_status='firing')[0]
        r1.status = 'resolved'
        r1.endsAt = self._alert_json['endsAt']
        r1.save()