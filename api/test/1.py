import re

alert_json = {
    "status":
    "firing",
    "labels": {
        "alertname": "InstanceDown",
        "instance": "test-exporter:10000",
        "job": "prometheus",
        "monitor": "codelab-monitor",
        "severity": "page"
    },
    "annotations": {
        "description":
        "test-exporter:10000 of job prometheus has been down for more than 5 minutes.",
        "summary": "Instance test-exporter:10000 down"
    },
    "startsAt":
    "2019-08-18T09:34:31.345816455Z",
    "endsAt":
    "0001-01-01T00:00:00Z",
    "generatorURL":
    "http://test-prometheus-58c75f5764-6rvjg:9090/graph?g0.expr=up+%3D%3D+0&g0.tab=1"
}

with open('msg-templates/firing-msg-template.md') as f:
    msg = f.read()
print(msg)
key_words = re.findall('\{\$(.*?)\}', msg)
print(key_words)
for key_word in key_words:
    print(key_word)
    if key_word in ['status', 'startsAt', 'endsAt', 'generatorURL']:
        msg = msg.replace('{$%s}' % key_word, alert_json[key_word])
    elif key_word in ['description', 'summary']:
        msg = msg.replace('{$%s}' % key_word,
                          alert_json['annotations'][key_word])
    else:
        msg = msg.replace('{$%s}' % key_word, alert_json['labels'][key_word])
    print(msg)
print(msg)